from fastapi import HTTPException, APIRouter

from ..schemas import MovieResponseModel, MovieRequestModel
from ..database import database as connection
from ..database import Movie

router= APIRouter(prefix='/movies')

@router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    with connection:
        if Movie.select().where(Movie.title == movie.title).first():
            raise HTTPException(status_code=409, detail='The title is in use or not valid')

        movie = Movie.create(
            title=movie.title
        )
        return movie