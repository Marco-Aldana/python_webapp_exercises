from fastapi.security import OAuth2PasswordRequestForm

from .routers import user_router, review_router, movie_router

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from .database import User, Movie, UserReview
from .database import database as connection
from .routers.common import create_access_token

app = FastAPI(title='Rotten Oranges',
              description="Project for post user movies critiques",
              version='1')

api_v1 = APIRouter(prefix='/api/v1')
api_v1.include_router(user_router)
api_v1.include_router(movie_router)
api_v1.include_router(review_router)


@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username or password not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )


app.include_router(api_v1)


@app.on_event('startup')
def startup():
    with connection:
        connection.create_tables([User, Movie, UserReview])


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
