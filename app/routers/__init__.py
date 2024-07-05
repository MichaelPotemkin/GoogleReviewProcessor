from fastapi import APIRouter

from . import google_reviews, health_check

api_router = APIRouter()
api_router.include_router(
    health_check.router, prefix="/health_check", tags=["Health Check"]
)
api_router.include_router(
    google_reviews.router, prefix="/google_reviews", tags=["Google Reviews"]
)
