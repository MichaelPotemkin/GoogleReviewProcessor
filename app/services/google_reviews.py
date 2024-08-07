import asyncio
import urllib.parse

import tldextract

from app.clients.google_reviews import GoogleReviewsClient
from app.schemas.google_reviews import (
    GoogleReviewsInputSchema,
    GoogleReviewsRequestSchema,
    GoogleReviewsResultsSchema,
    GoogleReviewsSchema,
)
from app.services.utilities import extract_domain


class GoogleReviewsService:
    def __init__(self):
        self.client = GoogleReviewsClient()

    @staticmethod
    def parse_results(data: GoogleReviewsSchema) -> GoogleReviewsResultsSchema:
        """Move the optional data to the top level of the dictionary for easier access"""
        for item in data.items:
            # Skip items without optional data
            if (
                "pagemap" not in item
                or "metatags" not in item["pagemap"]
                or not item["pagemap"]["metatags"]
            ):
                continue
            item["og:type"] = item["pagemap"]["metatags"][0].pop("og:type", None)
            item["og:locale"] = item["pagemap"]["metatags"][0].pop("og:locale", None)
            item["article:published_time"] = item["pagemap"]["metatags"][0].pop(
                "article:published_time", None
            )
        return GoogleReviewsResultsSchema(**data.model_dump())

    @classmethod
    def remove_duplicates(
        cls, data: GoogleReviewsResultsSchema
    ) -> GoogleReviewsResultsSchema:
        """Remove duplicate items from the data regardless of subdomains"""
        unique_items = []
        unique_main_domains = set()

        for item in data.items:
            main_domain = extract_domain(item.url_from, include_subdomain=False)
            if main_domain not in unique_main_domains:
                unique_items.append(item)
                unique_main_domains.add(main_domain)
            else:
                print(
                    f"Duplicate item found: {item.url_from}, which is a duplicate of the root domain {main_domain}"
                )

        return GoogleReviewsResultsSchema(items=unique_items)

    async def get_reviews_from_pages(
        self, request_data: GoogleReviewsInputSchema, number_of_pages: int = 10
    ) -> GoogleReviewsSchema:
        """Get reviews from all pages of the Google API"""
        result = GoogleReviewsSchema(items=[])
        responses = await asyncio.gather(
            *[
                self.client.get_reviews(
                    GoogleReviewsRequestSchema(**request_data.model_dump(), start=start)
                )
                for start in range(1, number_of_pages * 10 + 1, 10)
            ]
        )
        for response in responses:
            result.items.extend(response.items)
        return result

    async def get_reviews(
        self, request_data: GoogleReviewsInputSchema
    ) -> GoogleReviewsResultsSchema:
        google_reviews = await self.get_reviews_from_pages(
            request_data, number_of_pages=10
        )
        result = self.parse_results(google_reviews)
        return self.remove_duplicates(result)
