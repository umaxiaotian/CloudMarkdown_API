from peewee import *

db = MySQLDatabase(
    database='Cloudmarkdown',
    user='Cloudmarkdown',
    password="Cloudmarkdown",
    host="192.168.11.13",
    port=3306)

class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(100)
    password = CharField(100)
    refresh_token = TextField(null=True)

    class Meta:
        database = db

db.create_tables([User])

# ユーザーデータ挿入
User.create(name='tanaka', password='secret_tanaka')
User.create(name='kobayashi', password='secret_kobayashi')

