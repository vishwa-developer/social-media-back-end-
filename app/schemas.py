from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None