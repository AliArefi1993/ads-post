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


# class CategoryQuestionGetter(GetterDict):
#     def get(self, key: str, default: Any = None) -> Any:
#         if key in {'id', 'name'}:
#             return getattr(self._obj.category, key)
#         else:
#             return super(CategoryQuestionGetter, self).get(key, default)


# class CategoryNameWeight(BaseModel):
#     name: str = None
#     weight: float = None

#     class Config:
#         orm_mode = True
#         getter_dict = CategoryQuestionGetter


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

    class Config:
        orm_mode = True



# class CategoryQuestionBase(BaseModel):
#     id: int
#     weight: float



# class CategoryListUpdate(BaseModel):
#     categories: List[CategoryQuestionBase]
