from peewee import *

db = PostgresqlDatabase(
    'Cloudmarkdown',
    user='Cloudmarkdown',
    password='Cloudmarkdown',
    host='192.168.11.13',
    autocommit=True, 
    autorollback=True)

class Tags(Model):
    id = AutoField(primary_key=True)
    tag_name = CharField(unique=True)
    img = CharField(null=True)
    class Meta:
        database = db

db.create_tables([Tags])
# データ挿入
# Tags.create(tag_name='テストタグ')