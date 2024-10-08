from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing_extensions import Annotated


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True

class PostOut(Post):
    Post: int
    Votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserValidate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: id
    dir: Annotated[int, Field(strict=True, le=1)]
    class Config:
        arbitrary_types_allowed = True

