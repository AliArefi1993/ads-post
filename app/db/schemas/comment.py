from array import array
from typing import Optional, List
from pydantic.utils import GetterDict
from typing import Optional, List, Any

from pydantic import BaseModel, validator


# Comment
class CommentBase(BaseModel):
    text: str = None

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    ads_id: Optional[int] = None


class CommentUpdate(CommentBase):
    ads_id: Optional[int] = None


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True


class CommentDetail(CommentBase):
    id: int
    owner_id: Optional[int] = None
    ads_id: Optional[int] = None

    class Config:
        orm_mode = True
