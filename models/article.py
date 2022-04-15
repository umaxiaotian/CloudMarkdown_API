from peewee import *

db = MySQLDatabase(
    database='Cloudmarkdown',
    user='Cloudmarkdown',
    password="Cloudmarkdown",
    host="192.168.11.13",
    port=3306)
class Article(Model):
    id = AutoField(primary_key=True)
    title = CharField(500)
    detail = TextField(null=True)
    relate_user_id = TextField(null=True)
    good_count = IntegerField(default=0)
    post_date=DateTimeField(null=True)
    is_publish=BooleanField(default=False)
    class Meta:
        database = db

db.create_tables([Article])
# データ挿入
# Article.create(title='もえちゃん', detail='HELLO' ,relate_user_id=1, good_count=2)