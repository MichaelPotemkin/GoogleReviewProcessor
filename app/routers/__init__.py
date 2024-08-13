from fastapi import APIRouter

from . import health_check, valueserp_search

api_router = APIRouter()
api_router.include_router(
    health_check.router, prefix="/health_check", tags=["Health Check"]
)
api_router.include_router(
    valueserp_search.router, prefix="/valueserp", tags=["Valueserp API"]
)
