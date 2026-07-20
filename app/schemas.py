from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)



class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout 
    

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
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)