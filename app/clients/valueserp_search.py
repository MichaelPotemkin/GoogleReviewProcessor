from typing import Optional
from urllib.parse import urlencode

import aiohttp

from app.core.config import settings
from app.schemas.valueserp_search import (
    TimePeriodSchema,
    ValueserpRequestSchema,
    ValueserpResponseSchema,
)


class ValueserpClient:
    BASE_URL = "https://api.valueserp.com/search"
    API_KEY = settings.VALUESERP_API_KEY

    @classmethod
    def construct_url(
        cls,
        query: str,
        page: int,
        num: int,
        time_period: Optional[TimePeriodSchema] = None,
    ) -> str:
        """
        Construct the URL for the Valueserp API

        Parameters:
            query: str
                The search query
            page: int
                The page number
            num: int
                The number of results to return per page
            time_period: Optional[TimePeriodSchema]
                The time period to filter the search results by.

        Returns:
            str
                The constructed URL
        """
        params = {
            "api_key": cls.API_KEY,
            "q": query,
            "page": page,
            "num": num,
        }
        if time_period:
            params["time_period"] = "custom"
            params["time_period_min"] = time_period.min_time.date().strftime("%m-%d-%Y")
            params["time_period_max"] = time_period.max_time.date().strftime("%m-%d-%Y")

        return f"{cls.BASE_URL}?{urlencode(params)}"

    async def search(
        self,
        data: ValueserpRequestSchema,
    ) -> ValueserpResponseSchema:
        """
        Search for domains using the Valueserp API

        Parameters:
            data: ValueserpRequestSchema
                The request data

        Returns:
            ValueserpResponseSchema
                The response schema
        """
        url = self.construct_url(
            query=data.query,
            page=data.page,
            num=data.num,
            time_period=data.time_period,
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return ValueserpResponseSchema(**data)
