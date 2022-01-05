from typing import List

from fastapi import HTTPException, APIRouter, Response, Cookie, Depends
from fastapi.security import HTTPBasicCredentials

from .common import oauth2_sch, get_current_user
from ..schemas import UserResponseModel, UserRequestModel, ReviewResponseModel
from ..database import database as connection
from ..database import User

router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    with connection:
        if User.select().where(User.username == user.username).first():
            raise HTTPException(status_code=409, detail='The username is in use or not valid')

        hash_password = User.create_password(user.password)

        user = User.create(
            username=user.username,
            password=hash_password
        )
        return user


@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != User.create_password(credentials.password):
        raise HTTPException(status_code=404, detail="Password error")

    response.set_cookie(key='user_id', value=user.id)  # Token
    return user

"""
@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return [user_review for user_review in user.reviews]
"""
@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):
    return [user_review for user_review in user.reviews]
