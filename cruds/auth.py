from asyncio.windows_events import NULL
from contextlib import nullcontext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt

from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(name: str, password: str):
    """パスワード認証し、userを返却"""
    user = User.get(name=name)
    if user.password != password:
        raise HTTPException(status_code=401, detail='パスワード不一致')
    return user


def create_tokens(user_id: int):
    """パスワード認証を行い、トークンを生成"""
    # ペイロード作成
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
    }
    refresh_payload = {
        'token_type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=90),
        'user_id': user_id,
    }

    # トークン作成（本来は'SECRET_KEY123'はもっと複雑にする）
    access_token = jwt.encode(
        access_payload, 'SECRET_KEY123', algorithm='HS256')
    refresh_token = jwt.encode(
        refresh_payload, 'SECRET_KEY123', algorithm='HS256')

    # DBにリフレッシュトークンを保存
    User.update(refresh_token=refresh_token).where(
        User.id == user_id).execute()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


def get_current_user_from_token(token: str, token_type: str):
    """tokenからユーザーを取得"""
    # トークンをデコードしてペイロードを取得。有効期限と署名は自動で検証される。
    try:
        payload = jwt.decode(token, 'SECRET_KEY123', algorithms=['HS256'])
    except jwt.ExpiredSignatureError as e:
        # 有効期限切れ
        raise HTTPException(status_code=401, detail='Token_Expired')
    except jwt.InvalidTokenError as e:
        # decodeが実行できなかった
        raise HTTPException(status_code=401, detail='Decord_Fail_Error')
    except Exception as e:
        raise HTTPException(status_code=401, detail='Extract_Error')
    # トークンタイプが一致することを確認
    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    # DBからユーザーを取得
    user = User.get_by_id(payload['user_id'])

    # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
    if token_type == 'refresh_token' and user.refresh_token != token:
        print(user.refresh_token, '¥n', token)
        raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

    return user

def delete_token(user_id: int):
    # print(user_id)
    User.update(refresh_token=None).where(User.id == user_id).execute()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """アクセストークンからログイン中のユーザーを取得"""
    return get_current_user_from_token(token, 'access_token')


async def get_current_user_with_refresh_token(token: str = Depends(oauth2_scheme)):
    """リフレッシュトークンからログイン中のユーザーを取得"""
    return get_current_user_from_token(token, 'refresh_token')
