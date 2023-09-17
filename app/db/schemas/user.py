from array import array
from typing import Optional, List
from pydantic.utils import GetterDict
from typing import Optional, List, Any
from typing import Union

from pydantic import BaseModel, validator


# user
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    password: str


class UserUpdate(User):
    password: str


class User(User):
    id: int

    class Config:
        orm_mode = True


class UserDetail(User):
    id: int

    class Config:
        orm_mode = True
