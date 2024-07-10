from typing import Optional
from urllib.parse import urlencode

import aiohttp

from app.core.config import settings
from app.schemas.valueserp_search import TimePeriod, ValueserpResponseSchema, ValueserpRequestSchema


class ValueserpClient:
    BASE_URL = "https://api.valueserp.com/search"
    API_KEY = settings.VALUESERP_API_KEY

    @classmethod
    def construct_url(
            cls,
            query: str,
            page: int,
            num: int,
            time_period: Optional[TimePeriod] = None,
    ) -> str:
        params = {
            'api_key': cls.API_KEY,
            'q': query,
            'page': page,
            'num': num,
        }
        if time_period:
            params['time_period'] = 'custom'
            params['min_time'] = time_period.min_time
            params['max_time'] = time_period.max_time

        return f"{cls.BASE_URL}?{urlencode(params)}"

    async def search(
            self,
            data: ValueserpRequestSchema,
    ) -> ValueserpResponseSchema:
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
