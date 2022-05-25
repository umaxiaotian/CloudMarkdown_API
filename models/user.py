from peewee import *

db = PostgresqlDatabase(
    'Cloudmarkdown',
    user='Cloudmarkdown',
    password='Cloudmarkdown',
    host='Postgresql',
    autocommit=True, 
    autorollback=True)

class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    nickname = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(100)
    refresh_token = TextField(null=True)
    is_admin=BooleanField(default=False)
    avater = CharField(null=True)
    class Meta:
        database = db

db.create_tables([User])

# ユーザーデータ挿入
# User.create(name='tanaka', password='secret_tanaka')
# User.create(name='test1', nickname = 'テストユーザー１',password='test123',email='test1',avater='default.jpg')

