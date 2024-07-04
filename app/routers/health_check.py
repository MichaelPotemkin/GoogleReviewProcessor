from app.routers.google_reviews import router


@router.get("/health_check")
async def get_health_check():
    """
    Healthcheck endpoint to check if the service is alive.
    """
    return {"message": "Healthy"}
