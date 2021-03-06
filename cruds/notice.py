from peewee import *
from peewee import fn
from models.user import User
from models.notice import Notice
from cruds.auth import *

# 一般ユーザー　記事リスト取得

def getNotice():
    notices = []
    for notice in Notice.select().order_by(Notice.post_date.desc()):
        username = User.get(notice.relate_user_id)
        notices.append({"id":notice.id,"relate_user_id":notice.relate_user_id,"username":username.nickname,"title":notice.title,"detail":notice.detail,"post_date":notice.post_date})

    return notices