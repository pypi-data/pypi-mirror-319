import asyncio
from abc import abstractmethod
from typing import Protocol, TypedDict

import httpx

MAX_PAGE_COUNT = 150


class QueryParams(TypedDict):
    semester: str
    query_page_count: int


class QuerySender[P: QueryParams](Protocol):
    params: P
    client: httpx.AsyncClient

    def __init__(self, params: P, client: httpx.AsyncClient):
        self.params = params
        self.client = client

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def _query_page(self, query_page_idx: int) -> httpx.Response: ...

    @property
    def query_page_count(self) -> int:
        return self.params["query_page_count"]

    @property
    def semester(self) -> str:
        return self.params["semester"]

    async def get_pages(self, page_indices: list[int]) -> list[httpx.Response]:
        tasks = [self._query_page(i) for i in page_indices]
        responses = await asyncio.gather(*tasks)
        return responses
