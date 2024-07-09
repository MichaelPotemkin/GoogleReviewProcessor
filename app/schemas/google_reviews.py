from datetime import datetime
from typing import List, Optional

import dateparser
from pydantic import BaseModel, Field, field_validator, validator


class GoogleReviewItemSchema(BaseModel):
    """
    Schema for Google Review Item

    Attributes:
        type: str
            The type of the item
        page_from_title: str
            The title of the page
        url_from: str
            The url of the page
        domain_from: str
            The domain of the page
        item_type: str
            The type of the item
        page_from_language: str
            The language of the page
        published_date: datetime
            The published date of the item
    """

    type: str = Field(alias="kind")
    page_from_title: str = Field(alias="title")
    url_from: str = Field(alias="link")
    domain_from: str = Field(alias="displayLink")
    item_type: Optional[str] = Field(alias="og:type", default=None)
    page_from_language: Optional[str] = Field(alias="og:locale", default=None)
    published_date: Optional[datetime] = Field(
        alias="article:published_time", default=None
    )

    @field_validator("published_date", mode="before")
    def parse_published_date(cls, value):
        if value is None:
            return value
        return dateparser.parse(value)


class GoogleReviewsSchema(BaseModel):
    items: List[dict]


class GoogleReviewsInputSchema(BaseModel):
    """
    Schema for Google Reviews Input

    Attributes:
        query: str
            The search query
        cx: str
            The custom search engine id
        sort: Optional[str]
            The sort parameter
    """

    query: str
    cx: str
    sort: Optional[str] = None


class GoogleReviewsRequestSchema(GoogleReviewsInputSchema):
    """
    Schema for preforming the request to the Google Reviews API

    Attributes:
        start: int
            The start index. Should be between 1 and 100
    """

    start: int = 1

    @field_validator("start")
    def validate_start(cls, v):
        if not 1 <= v <= 100:
            raise ValueError("Start must be between 1 and 100")
        return v


class GoogleReviewsResultsSchema(BaseModel):
    items: list[GoogleReviewItemSchema]
