import array
from ast import dump
from multiprocessing.dummy import Array
from click import echo
from models.article import Article
from cruds.auth import *


def getArticleList():
    # 記事情報を取得
    query = Article.select().get()
    articles = []
    for article in query.select().order_by(Article.good_count.desc()).limit(10):
        articles.append(
            {"id": article.id, "title": article.title, "detail": article.detail, "tags": article.tags, "post_date": article.post_date})

    return articles


def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = ["list"]
    for article in query.select().where(Article.relate_user_id == user_id).order_by(Article.post_date.desc()):
        articles.append(
            {"id": article.id, "title": article.title, "detail": article.detail, "tags": article.tags, "post_date": article.post_date})

    return articles
