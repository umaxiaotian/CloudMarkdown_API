from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from cruds.auth import *
from cruds.article import *

app = FastAPI()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Article(BaseModel):
    name: str

    class Config:
        orm_mode = True

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)

@app.get("/refresh_token/", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

@app.get("/")
async def say_hello(user: User = Depends(get_current_user)):
	return {"Hello": "World"}

@app.get("/list")
async def return_article_list(article: Article = Depends(getArticleList),user: User = Depends(get_current_user)):
    return article

