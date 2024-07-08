import aiohttp

from app.core.config import settings
from app.schemas.google_reviews import GoogleReviewsRequestSchema, GoogleReviewsSchema


class GoogleReviewsClient:
    """Class to interact with the Google Reviews API"""

    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    API_KEY = settings.GOOGLE_API_KEY

    @classmethod
    def construct_url(cls, query: str, cx: str, sort: str, start: int = 1) -> str:
        if not 1 <= start <= 100:
            raise ValueError("Start must be between 1 and 100")
        return f"{cls.BASE_URL}?key={cls.API_KEY}&q={query}&cx={cx}&sort={sort}&start={start}"

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
