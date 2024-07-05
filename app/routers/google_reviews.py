from typing import Optional

from fastapi import APIRouter, Depends

from app.schemas.google_reviews import (
    GoogleReviewsInputSchema,
    GoogleReviewsResultsSchema,
)
from app.services.google_reviews import GoogleReviewsService

router = APIRouter()


@router.get(
    "/reviews", response_model_by_alias=False, response_model=GoogleReviewsResultsSchema
)
async def get_reviews(
    query: str,
    cx: str,
    sort: Optional[str] = None,
    service: GoogleReviewsService = Depends(GoogleReviewsService),
):
    """
    Get reviews from Google API

    Parameters:
        query: str
            The search query
        cx: str
            The custom search engine id
        sort: Optional[str]
            The sort parameter
    """
    data = GoogleReviewsInputSchema(query=query, cx=cx, sort=sort)
    result = await service.get_reviews(data)
    return result
