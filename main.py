from fastapi import Depends, FastAPI, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cruds.auth import *
from cruds.article import *

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)
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
    id: int
    title: str
    detail: str
    relate_user_id: str
    good_count: int
    post_date: str

    class Config:
        orm_mode = True

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    print(form.username)
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)

@app.get("/refresh_token/", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)

@app.get("/user/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

@app.put("/user/logout/")
async def delete(user_id: User = Depends(get_current_user)):
    # print(user_id)
    delete_token(user_id)
    return {"detail": "Success"}

@app.get("/article/list/")
async def return_article_list(article: Article = Depends(getArticleList)):
    return article

# 検索機能
@app.get("/article/search/{search_text}")
async def search_article_list(article: Article = Depends(searchArticleList)):
    return article

@app.get("/article/tags/list")
async def getTagList(tags: Article = Depends(getTagList)):
    return tags


@app.get("/article/{article_id}")
async def return_article_detail(article: Article = Depends(getArticleDetail)):
    return article

@app.get("/user/article/list")
async def return_my_article_list(articles: Article = Depends(getMyArticleList)):
    return articles
