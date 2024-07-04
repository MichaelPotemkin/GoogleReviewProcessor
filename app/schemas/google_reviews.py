from pydantic import BaseModel


class GoogleReviewsInputSchema(BaseModel):
    q: str


class GoogleReviewsSchema(BaseModel):
    pass
