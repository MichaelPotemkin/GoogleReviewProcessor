from fastapi import APIRouter

from . import auth, health_check, via

api_router = APIRouter()
api_router.include_router(health_check.router, tags=["Health Check"])
api_router.include_router(via.router, prefix="/api", tags=["API"])
api_router.include_router(auth.router, prefix="/user", tags=["Authentication"])
