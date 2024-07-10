from typing import Optional
from urllib.parse import urlencode

import aiohttp

from app.core.config import settings
from app.schemas.google_reviews import GoogleReviewsRequestSchema, GoogleReviewsSchema


class GoogleReviewsClient:
    """Class to interact with the Google Reviews API"""

    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    API_KEY = settings.GOOGLE_API_KEY

    @classmethod
    def construct_url(
            cls, query: str, cx: str, sort: Optional[str] = None, start: Optional[int] = 1
    ) -> str:
        if not 1 <= start <= 100:
            raise ValueError("Start must be between 1 and 100")

        params = {
            'key': cls.API_KEY,
            'q': query,
            'cx': cx,
            'start': start
        }

        if sort:
            params['sort'] = sort

        result = f"{cls.BASE_URL}?{urlencode(params)}"

        return result

    async def get_reviews(
        self, request_data: GoogleReviewsRequestSchema
    ) -> GoogleReviewsSchema:
        url = self.construct_url(
            query=request_data.query,
            cx=request_data.cx,
            sort=request_data.sort,
            start=request_data.start,
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                items = data.get("items", [])
                return GoogleReviewsSchema(items=items)
