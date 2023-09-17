from array import array
from typing import Optional, List
from pydantic.utils import GetterDict
from typing import Optional, List, Any

from pydantic import BaseModel, validator


# Ads
class AdsBase(BaseModel):
    title: str
    text: str = None
    pic_path: Optional[str] = None

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    id: int
    text: str
    owner_id: int


class AdsCreate(AdsBase):
    pass


class AdsUpdate(AdsBase):
    pass


class Ads(AdsBase):
    id: int

    class Config:
        orm_mode = True


class AdsDetail(AdsBase):
    id: int
    owner_id: Optional[int] = None
    comments: List[CommentSchema] = []

    class Config:
        orm_mode = True


# class CategoryQuestionBase(BaseModel):
#     id: int
#     weight: float


# class CategoryListUpdate(BaseModel):
#     categories: List[CategoryQuestionBase]
