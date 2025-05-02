from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import Field


#               ---------------- USER SCHEMA ----------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#               ---------------- POST SCHEMA ----------------
class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostsBase):
    pass

class PostOut(PostsBase):
    id: int
    user_id: int
    owner: UserOut

    model_config = {
        "from_attributes": True
    }


#               ---------------- AUTH SCHEMA ----------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


#               ---------------- AUTH SCHEMA ----------------
class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1)