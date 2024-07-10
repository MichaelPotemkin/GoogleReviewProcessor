from typing import Optional

from fastapi import APIRouter, Depends

from app.schemas.valueserp_search import ValueserpSearchResultsSchema, ValueserpInputSchema
from app.services.valueserp_search import ValueserpService

router = APIRouter()


@router.get(
    "/search", response_model_by_alias=False, response_model=ValueserpSearchResultsSchema
)
async def search(
    query: str,
    # TODO: add dates
    service: ValueserpService = Depends(ValueserpService),
):
    """
    Get domains from the Valueserp API

    Parameters:
        query: str
            The search query
    """
    data = ValueserpInputSchema(query=query)
    result = await service.search(data)
    return result
