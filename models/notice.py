from peewee import *

db = PostgresqlDatabase(
    'Cloudmarkdown',
    user='Cloudmarkdown',
    password='Cloudmarkdown',
    host='localhost',
    autocommit=True, 
    autorollback=True)

class Notice(Model):
    id = AutoField(primary_key=True)
    relate_user_id = IntegerField(null=True)
    title = CharField(500)
    detail = TextField(null=True)
    post_date=DateTimeField(null=True)
    class Meta:
        database = db

db.create_tables([Notice])
# データ挿入
# Notice.create(tag_name='テストタグ')