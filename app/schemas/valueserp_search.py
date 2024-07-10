from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, model_validator, Field, field_validator


class TimePeriod(BaseModel):
    min_time: datetime
    max_time: datetime

    @model_validator(mode="after")
    def validate_time_period(self):
        if self.min_time > self.max_time:
            raise ValueError("min_time must be less than max_time")

        return self


class ValueserpItemSchema(BaseModel):
    """
    Schema for a single item in the Valueserp API results.
    """
    page_from_title: str = Field(alias="title")
    url_from: str = Field(alias="link")
    domain_from: str = Field(alias="domain")


class ValueserpSearchResultsSchema(BaseModel):
    """
    Output Schema for Valueserp API Results. Contains a list of filtered results from the Valueserp API.

    Attributes:
        items: list[GoogleReviewItemSchema]
            The list of items
    """
    items: List[ValueserpItemSchema]


class ValueserpPageSchema(BaseModel):
    """
    Schema for a single page in the Valueserp API pagination.
    """
    page: int
    link: str


class ValueserpAPIPaginationSchema(BaseModel):
    """
    Pagination schema for Valueserp API.
    """
    next: Optional[str]
    other_pages: Optional[List[ValueserpPageSchema]]


class ValueserpPaginationSchema(BaseModel):
    """
    Pagination schema for Valueserp API.
    """
    api_pagination: ValueserpAPIPaginationSchema


class ValueserpResponseSchema(BaseModel):
    """
    Schema for Valueserp Response.

    Attributes:
        pagination: ValueserpPaginationSchema
            The pagination information
        items: List[dict]
            The list of search results
    """
    pagination: ValueserpPaginationSchema
    items: Optional[List[ValueserpItemSchema]] = Field(alias="organic_results", default=[])


class ValueserpInputSchema(BaseModel):
    """
    Input Schema for Valueserp API.

    Attributes:
        query: str
            The search query
        time_period: Optional[TimePeriod]
            The time period to filter the search results by.
    """
    query: str
    time_period: Optional[TimePeriod] = None


class ValueserpRequestSchema(ValueserpInputSchema):
    """
    Schema for Valueserp Request.

    Attributes:
        page: Optional[int]
            The page number
        num: Optional[int]
            The number of results to return per page
    """
    page: Optional[int] = 1
    num: Optional[int] = 100

    @field_validator("num")
    def validate_num(cls, value):
        if not 1 <= value <= 100:
            raise ValueError("num must be between 1 and 100")
        return value
