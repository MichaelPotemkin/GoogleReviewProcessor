from operator import xor
from typing import Optional

import dateparser
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.valueserp_search import (
    TimePeriodSchema,
    ValueserpInputSchema,
    ValueserpSearchResultsSchema,
)
from app.services.valueserp_search import ValueserpService

router = APIRouter()


@router.get(
    "/search",
    response_model_by_alias=False,
    response_model=ValueserpSearchResultsSchema,
)
async def search(
    query: str,
    min_time: Optional[str] = None,
    max_time: Optional[str] = None,
    service: ValueserpService = Depends(ValueserpService),
):
    """
    Get domains from the Valueserp API

    Parameters:
        query: str
            The search query
    """
    try:
        if xor(min_time is None, max_time is None):
            raise ValueError(
                "Both min_time and max_time must be provided if one is provided."
            )
        time_period = None
        if min_time and max_time:
            min_time = dateparser.parse(min_time)
            max_time = dateparser.parse(max_time)
            time_period = TimePeriodSchema(min_time=min_time, max_time=max_time)
        data = ValueserpInputSchema(query=query, time_period=time_period)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    result = await service.search(data)
    return result
