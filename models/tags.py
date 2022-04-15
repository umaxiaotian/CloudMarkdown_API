from peewee import *

db = MySQLDatabase(
    database='Cloudmarkdown',
    user='Cloudmarkdown',
    password="Cloudmarkdown",
    host="192.168.11.13",
    port=3306)
class Tags(Model):
    id = AutoField(primary_key=True)
    tag_name = CharField(500)
    class Meta:
        database = db

db.create_tables([Tags])
# データ挿入
# Tags.create(tag_name='テストタグ')