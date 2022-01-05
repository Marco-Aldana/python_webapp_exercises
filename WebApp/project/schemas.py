import datetime

from peewee import ModelSelect
from pydantic import BaseModel, Field, validator
from pydantic.utils import GetterDict
from typing import Any


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# User--------------------------------------------------------------------------
class UserRequestModel(BaseModel):
    username: str = Field(max_length=50, min_length=3)
    password: str = Field(max_length=50, min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "User",
                "password": "Pass1234"
            }
        }

    # @validator('username')
    # def username_validator(cls, username):
    #    if len(username)<3 or len(username)>50:
    #        raise ValueError('The lenght must be between 3 and 50 characters')
    #    return username


class UserResponseModel(ResponseModel):
    id: int
    username: str = Field(max_length=50, min_length=3)


class MovieRequestModel(BaseModel):
    title: str = Field(max_length=50, min_length=3)

    class Config:
        schema_extra = {
            "example": {
                "title": "The movie"
            }
        }


# Movie-------------------------------------------------
class MovieResponseModel(ResponseModel):
    id: int
    title: str = Field(max_length=50, min_length=3)

# Review------------------------------------------------
class ReviewRequestModel(BaseModel):
    movie_id: int
    review: str = Field(min_length=70)
    score: int = Field(le=5, ge=1)

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "review": "Excellent movie. bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla",
                "score": 1
            }
        }


class ReviewResponseModel(ResponseModel):
    id: int
    user_id: int
    movie: MovieResponseModel
    review: str = Field(min_length=70)
    score: int = Field(le=5, ge=1)
    created_at: datetime.datetime


class ReviewRequestPutModel(BaseModel):
    review: str = Field(min_length=70)
    score: int = Field(le=5, ge=1)
