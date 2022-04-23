import array
from peewee import *
from peewee import fn
from ast import dump
from multiprocessing.dummy import Array
from pickle import TRUE
from click import echo
from models.article import Article
from models.user import User
from models.tags import Tags
from models.relate_tags import Relate_Tags
from cruds.auth import *

# 一般ユーザー　記事リスト取得


def getArticleList():
    # 記事情報を取得
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.is_publish == TRUE).order_by(Article.good_count.desc()).limit(10):
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": article.good_count,  "post_date": article.post_date})
    return articles

# 一般ユーザー　記事内容取得


def getArticleDetail(article_id: int):
    article = Article.select().where(Article.is_publish == TRUE,
                                     Article.id == article_id).get()
    relate_user_name = User.get(article.relate_user_id).nickname
    tags = []
    # 関連するタグを取得
    for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
        tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
    return {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": article.good_count, "post_date": article.post_date}


def searchArticleList(search_text: str):
    # 検索記事内容を取得
    articles = []
    for article in Article.select().where(Article.is_publish == TRUE, Article.title.contains(search_text)).order_by(Article.good_count.desc()):
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": article.good_count,  "post_date": article.post_date})
    return articles

# タグリスト一覧を取得する


def getTagList():
    relate_tags = []
    for tag in Relate_Tags.select(Tags, fn.Count(Relate_Tags.tag_id)).join(Tags).group_by(Tags).where(Relate_Tags.tag_id == Tags.id).order_by(fn.Count(Relate_Tags.tag_id).desc()):
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
        tags = []
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append({"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name,
                        "tags": tags, "title": article.title, "good_count": article.good_count,  "post_date": article.post_date})
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
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title,  "good_count": article.good_count, "post_date": article.post_date})

    return articles


# 会員ページ＿自身の記事リスト


def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id).order_by(Article.create_date.desc()):
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).nickname
        articles.append(
            {"id": article.id, "relate_user": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": article.good_count, "is_publish": article.is_publish, "post_date": article.post_date, "create_date": article.create_date})

    return articles

# 会員ページ＿自身の記事


def getUserArticleDetail(article_id: int, user_id: User = Depends(get_current_user)):
    article = Article.select().where(Article.id == article_id).get()
    relate_user_name = User.get(article.relate_user_id).nickname
    tags = []
    # 関連するタグを取得
    for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
        tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
    return {"id": article.id, "relate_user_id": article.relate_user_id, "img": article.img, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": article.good_count, "is_publish": article.is_publish, "post_date": article.post_date}
