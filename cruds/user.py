from pickle import TRUE
from fastapi import Depends, Form ,HTTPException
from models.user import User
from cruds.auth import *
def updateUserProfile(name: str = Form(...),email: str = Form(...),nickname: str = Form(...),avater: str = Form(...),user_id: User = Depends(get_current_user)):
    if(avater != 'null'):
        User.update(avater=avater).where(User.id == user_id).execute()

    result = User.get_or_none(User.name==name)
    if(result != user_id):
        raise HTTPException(status_code=401, detail=f'すでにこのユーザー名は使われています。')

    result = User.get_or_none(User.nickname==nickname)
    if(result != None and result != user_id):
        raise HTTPException(status_code=401, detail=f'すでにこのニックネームは使われています。')

    update_id = User.update(name=name, email=email,nickname=nickname).where(User.id == user_id).execute()
    
    if(update_id):
        return TRUE

def updateUserPassword(current_pw: str = Form(...),new_pw: str = Form(...),user_id: User = Depends(get_current_user)):
    pwCheck = User.get_or_none(User.id == user_id,User.password == current_pw)
    if(pwCheck == None):
        raise HTTPException(status_code=401, detail=f'現在のパスワードが正しくありません')
    if(pwCheck == user_id):
        if(current_pw == new_pw):
            raise HTTPException(status_code=401, detail=f'現在のパスワードと同一です')
        update_id = User.update(password=new_pw,).where(User.id == user_id).execute()
        if(update_id):
            return TRUE