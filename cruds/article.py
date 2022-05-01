import datetime
from fastapi import Depends, Form
from peewee import *
from peewee import fn
from pickle import TRUE
from models.article import Article
from models.user import User
from models.tags import Tags
from models.relate_tags import Relate_Tags
from models.relate_good_count import Relate_Good_Count
from cruds.auth import *
import json

# 一般ユーザー　記事リスト取得
def postArticle(title: str = Form(...),filename: str = Form(...),selection_tag: str = Form(...),define_editor_text: str = Form(...),user_id: User = Depends(get_current_user)):
    dt_now = datetime.now()
    if(define_editor_text == 'null'):
        define_editor_text=''
    if(filename == 'null'):
        filename="default.jpg"
    new_article_id = Article.insert(title=title, detail=define_editor_text,img=filename,relate_user_id=user_id,create_date=dt_now).execute()
    if(selection_tag != 'null'):
        for tag in json.loads(selection_tag):
            tag_id = Tags.select().where(Tags.tag_name==tag).get()
            print(tag_id)
            Relate_Tags.insert(article_id=new_article_id,tag_id=tag_id).execute()

    return new_article_id

def addGoodCount(article_id,user_id: User = Depends(get_current_user)):
    is_good=Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article_id,Relate_Good_Count.user_id == user_id).get().count
    if(is_good == 0):
        Relate_Good_Count.insert(article_id=article_id,user_id=user_id).execute()
        return {'detail':'Finished_Good'}
    else:
        return {'detail':'Already_Good'}

def removeGoodCount(article_id,user_id: User = Depends(get_current_user)):
    exec = Relate_Good_Count.delete().where(Relate_Good_Count.article_id == article_id,Relate_Good_Count.user_id == user_id).execute()
    if(exec == 1):
        return {'detail':'Finished_Remove'}
    else:
        return {'detail':'Remove_Missing'}
  
def updateArticle(article_id,title: str = Form(...),filename: str = Form(...),selection_tag: str = Form(...),define_editor_text: str = Form(...),user_id: User = Depends(get_current_user)):
    dt_now = datetime.now()
    if(define_editor_text == 'null'):
        define_editor_text=''
    if(filename == 'null'):
        filename="default.jpg"
    update_id = Article.update(title=title, detail=define_editor_text,img=filename,relate_user_id=user_id,create_date=dt_now).where(Article.id == article_id,Article.relate_user_id ==user_id).execute()
    if(selection_tag != 'null'):
        #一度すべてのタグを削除
        Relate_Tags.delete().where(Relate_Tags.article_id == article_id).execute()
        #タグの書き込み
        for tag in json.loads(selection_tag):
            tag_id = Tags.select().where(Tags.tag_name==tag).get()
            Relate_Tags.insert(article_id=article_id,tag_id=tag_id).execute()

    return update_id

def publishArticle(article_id,user_id: User = Depends(get_current_user)):
    dt_now = datetime.now()
    update_id = Article.update(is_publish=1,post_date=dt_now,create_date=dt_now).where(Article.id == article_id,Article.relate_user_id ==user_id).execute()

    return update_id

def disPublishArticle(article_id,user_id: User = Depends(get_current_user)):
    dt_now = datetime.now()
    update_id = Article.update(is_publish=0,post_date=dt_now,create_date=dt_now).where(Article.id == article_id,Article.relate_user_id ==user_id).execute()

    return update_id

def deleteArticle(article_id,user_id: User = Depends(get_current_user)):
    Relate_Tags.delete().where(Relate_Tags.article_id == article_id).execute()
    Relate_Good_Count.delete().where(Relate_Good_Count.article_id == article_id).execute()
    update_id = Article.delete().where(Article.id == article_id,Article.relate_user_id ==user_id).execute()

    return update_id



def getArticleList():
    # 記事情報を取得

    articles = []
    for article in Article.select(Article).join(Relate_Good_Count).where(Article.is_publish == TRUE).group_by(Article).order_by(fn.Count(Relate_Good_Count.article_id).desc()).limit(10):
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
        print(count)
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": count,  "post_date": article.post_date})
    return articles

# 一般ユーザー　記事内容取得


def getArticleDetail(article_id: int):
    article = Article.select().where(Article.is_publish == TRUE,
                                     Article.id == article_id).get()
    relate_user_name = User.get(article.relate_user_id).nickname
    count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
    tags = []
    # 関連するタグを取得
    for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
        tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
    return {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": count, "post_date": article.post_date}


def searchArticleList(search_text: str):
    # 検索記事内容を取得
    articles = []
    for article in Article.select().where(Article.is_publish == TRUE, Article.title.contains(search_text)).order_by(Article.good_count.desc()):
        count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": count,  "post_date": article.post_date})
    return articles

# タグリスト一覧を取得する


def getTagList():
    relate_tags = []
    for tag in Relate_Tags.select(Tags, fn.Count(Relate_Tags.tag_id)).join(Tags).join(Article,on=(Relate_Tags.article_id == Article.id)).group_by(Tags).where(Relate_Tags.tag_id == Tags.id,Article.is_publish == True).order_by(fn.Count(Relate_Tags.tag_id).desc()).limit(10):
        print(tag)
        relate_tags.append(
            {"id": tag.tag_id.id, "tag_name": tag.tag_id.tag_name, "img": tag.tag_id.img, "post_count": tag.count})

    return relate_tags
# タグリスト一覧を取得する


def getTagListAll():
    relate_tags = []
    for tag in Tags.select():
        relate_tags.append(
            {"id": tag.id, "tag_name": tag.tag_name, "img": tag.img})

    return relate_tags

# タグに関連する記事一覧を取得する


def getRelateTagArticleList(tag_id: int):
    articles = []
    for article in Article.select().join(Relate_Tags).where(Relate_Tags.article_id == Article.id, Relate_Tags.tag_id == tag_id, Article.is_publish == TRUE):
        count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
        tags = []
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append({"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name,
                        "tags": tags, "title": article.title, "good_count": count,  "post_date": article.post_date})
    return articles

# タグIDからタグ名などを取得


def getTagName(tag_id: int):
    tag = Tags.get(tag_id)
    return {"id": tag.id, "tag_name": tag.tag_name, "img": tag.img}

# タグIDからタグ名などを取得


def getMemberUser(user_id: int):
    user = User.get(user_id)
    return {"id": user.id, "nickname": user.nickname, "avater": user.avater}


def getUserArticle(user_id: int):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id, Article.is_publish == TRUE).order_by(Article.post_date.desc()):
        count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title,  "good_count": count, "post_date": article.post_date})

    return articles


# 会員ページ＿自身の記事リスト


def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id).order_by(Article.id.desc()):
        count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": count, "is_publish": article.is_publish, "post_date": article.post_date, "create_date": article.create_date})

    return articles

# 会員ページ＿自身の記事


def getUserArticleDetail(article_id: int, user_id: User = Depends(get_current_user)):
    article = Article.select().where(Article.id == article_id).get()
    count= Relate_Good_Count.select(fn.Count(Relate_Good_Count.article_id)).where(Relate_Good_Count.article_id == article.id).get().count
    relate_user_name = User.get(article.relate_user_id).nickname
    tags = []
    # 関連するタグを取得
    for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
        tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
    return {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": count, "is_publish": article.is_publish, "post_date": article.post_date}
