from typing import List

from fastapi import APIRouter, HTTPException, Depends

from .common import get_current_user
from ..schemas import ReviewRequestPutModel, ReviewResponseModel, ReviewRequestModel
from ..database import database as connection
from ..database import User, UserReview, Movie

router = APIRouter(prefix='/reviews')


@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel, user: User = Depends(get_current_user)):
    with connection:
        if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
            raise HTTPException(status_code=404, detail="movie not found")

        user_review = UserReview.create(
            user=user.id,
            movie=user_review.movie_id,
            review=user_review.review,
            score=user_review.score
        )
        return user_review


@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    return [user_review for user_review in reviews]


@router.get('/{id_review}', response_model=ReviewResponseModel)
async def get_review(id_review: int):
    user_review = UserReview.select().where(UserReview.id == id_review).first()
    if not user_review:
        raise HTTPException(status_code=404, detail="review not found")
    return user_review


@router.put('/{id_review}', response_model=ReviewResponseModel)
async def update_review(id_review: int, review_request: ReviewRequestPutModel, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == id_review).first()
    if not user_review:
        raise HTTPException(status_code=404, detail="review not found")

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not able to modify this review")

    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review


@router.delete('/{id_review}', response_model=ReviewResponseModel)
async def delete_review(id_review: int, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == id_review).first()
    if not user_review:
        raise HTTPException(status_code=404, detail="review not found")

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not able to delete this review")


    user_review.delete_instance()

    return user_review
