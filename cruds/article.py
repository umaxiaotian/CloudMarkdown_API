from models.article import Article
from cruds.auth import *

def getArticleList():
    # 記事情報を取得
    query = Article.select().get()
    article = []
    for user in query.select().order_by(Article.good_count.desc()).limit(10):
        article.append(user)

    return article

def getMyArticleList(user_id: User = Depends(get_current_user)):
    query = Article.select().get()
    articles = []
    for article in query.select().where(Article.relate_user_id == user_id):
        articles.append(article)

    return articles
