from peewee import *

from models.article import Article
from models.user import User
db = PostgresqlDatabase(
    'Cloudmarkdown',
    user='Cloudmarkdown',
    password='Cloudmarkdown',
    host='Postgresql',
    autocommit=True, 
    autorollback=True)
class Relate_Good_Count(Model):
    id = AutoField(primary_key=True)
    article_id = ForeignKeyField(Article) #外部キー
    user_id=ForeignKeyField(User)


    class Meta:
        database = db

db.create_tables([Relate_Good_Count])
# データ挿入
# Relate_Good_Count.create(article_id=1, tag_id=1)