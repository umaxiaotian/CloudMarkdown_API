from cgitb import text
from getpass import getuser
from fastapi import Depends, FastAPI, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cruds.auth import *
from cruds.article import *
from cruds.notice import *

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
    email: str
    nickname: str
    avater: str = None

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

class Notice(BaseModel):
    id: int
    relate_user: int = None
    title: str
    detail: str
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
async def read_users_me(user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return user

@app.put("/user/logout/")
async def delete(user_id: User = Depends(get_current_user)):
    # print(user_id)
    delete_token(user_id)
    return {"detail": "Success"}

#ユーザーの記事リスト
@app.get("/user/article/list")
async def return_my_article_list(articles: Article = Depends(getMyArticleList)):
    return articles

#お知らせ
@app.get("/notice/list/")
async def return_article_list(article: Notice = Depends(getNotice)):
    return article

#記事リスト
@app.get("/article/list/")
async def return_article_list(article: Article = Depends(getArticleList)):
    return article

# 検索機能
@app.get("/article/search/{search_text}")
async def search_article_list(article: Article = Depends(searchArticleList)):
    return article

# タグリスト（使用頻度が多い順）
@app.get("/article/tags/list")
async def getTagList(tags: Article = Depends(getTagList)):
    return tags

# タグに関連する記事一覧を取得する
@app.get("/article/tag/{tag_id}")
async def getTagList(article_list: Article = Depends(getRelateTagArticleList)):
    return article_list

# タグidからタグ名を取得
@app.get("/tag/name/{tag_id}")
async def getTagList(tag_name: Article = Depends(getTagName)):
    return tag_name

@app.get("/member/user/{user_id}")
async def getTagList(user: Article = Depends(getMemberUser)):
    return user


@app.get("/article/{article_id}")
async def return_article_detail(article: Article = Depends(getArticleDetail)):
    return article

@app.get("/article/user/{user_id}")
async def return_article_detail(article: Article = Depends(getUserArticle)):
    return article


