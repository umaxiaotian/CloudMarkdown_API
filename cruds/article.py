from models.article import Article

def getArticleList():
    # 記事情報を取得
    query = Article.select().get()
    article = []
    for user in query.select().order_by(Article.good_count.desc()).limit(10):
        article.append(user)

    return article