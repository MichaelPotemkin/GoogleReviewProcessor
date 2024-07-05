from fastapi import FastAPI

from app.routers import api_router

app = FastAPI(
    title="GoogleReviewProcessor API",
)
app.include_router(api_router, prefix="/v1")
