import asyncio
from typing import List

from app.clients.valueserp_search import ValueserpClient
from app.schemas.valueserp_search import (
    ValueserpInputSchema,
    ValueserpRequestSchema,
    ValueserpResponseSchema,
    ValueserpSearchResultsSchema,
)
from app.services.utilities import extract_domain


class ValueserpService:
    def __init__(self):
        self.client = ValueserpClient()

    @staticmethod
    def parse_results(
        data: List[ValueserpResponseSchema],
    ) -> ValueserpSearchResultsSchema:
        """
        Parse the results from the Valueserp API requests and return a model with the items.
        """
        return ValueserpSearchResultsSchema(
            items=[item for response in data for item in response.items]
        )

    @staticmethod
    def remove_duplicates(
        data: ValueserpSearchResultsSchema,
    ) -> ValueserpSearchResultsSchema:
        """
        Remove duplicate items from the data by root domain.
        """
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

        return ValueserpSearchResultsSchema(items=unique_items)

    async def search(self, data: ValueserpInputSchema) -> ValueserpSearchResultsSchema:
        """
        Search for domains using the Valueserp API.
        """
        initial_request_data = ValueserpRequestSchema(**data.model_dump())
        initial_response = await self.client.search(initial_request_data)

        other_pages = initial_response.pagination.api_pagination.other_pages
        responses = [initial_response]
        if other_pages:
            additional_responses = await asyncio.gather(
                *[
                    self.client.search(
                        ValueserpRequestSchema(**data.model_dump(), page=page.page)
                    )
                    for page in other_pages
                ]
            )
            responses.extend(additional_responses)

        result = self.parse_results(responses)
        return self.remove_duplicates(result)
