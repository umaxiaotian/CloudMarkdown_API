import array
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
        relate_user_name = User.get(article.relate_user_id).name
        articles.append(
            {"id":article.id,"relate_user_id": article.relate_user_id, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "good_count": article.good_count,  "post_date": article.post_date})
    return articles

# 一般ユーザー　記事内容取得
def getArticleDetail(article_id: int):
    article = Article.select().where(Article.is_publish == TRUE,
                                     Article.id == article_id).get()
    relate_user_name = User.get(article.relate_user_id).name
    tags = []
    # 関連するタグを取得
    for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
        tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
    return {"id":article.id,"relate_user_id": article.relate_user_id, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": article.good_count, "post_date": article.post_date}


# 会員ページ＿自身の記事リスト
def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id).order_by(Article.post_date.desc()):
        tags = []
        # 関連するタグを取得
        for tag in Tags.select().join(Relate_Tags).where(Tags.id == Relate_Tags.tag_id, Relate_Tags.article_id == article.id):
            tags.append({"tag_id": tag.id, "tag_name": tag.tag_name})
        relate_user_name = User.get(article.relate_user_id).name
        articles.append(
            {"id":article.id,"relate_user": article.relate_user_id, "relate_user_name": relate_user_name, "tags": tags, "title": article.title, "detail": article.detail, "good_count": article.good_count, "post_date": article.post_date})

    return articles
