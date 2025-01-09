from __future__ import annotations

import typing
from enum import Enum
from typing import TypedDict, override

import httpx
from bs4 import BeautifulSoup
from loguru import logger

from .query_sender import QueryParams, QuerySender
from .utils import get_current_semester, to_str_dict

if typing.TYPE_CHECKING:
    pass


class QueryType(Enum):
    TITLE = 1
    """課程名稱"""
    DOMAIN = 9
    """領域專長"""
    INSTRUCTOR = 2
    """教師姓名"""
    CODE = 3
    """課號"""
    IDENTIFIER = 5
    """課程識別碼"""
    SERIAL = 4
    """流水號"""


class Params(TypedDict):
    current_sem: str
    """學期"""
    cstype: int
    """查詢類型"""
    csname: str
    """查詢值"""
    alltime: str
    """全部時間"""
    allproced: str
    """全部節次"""
    allsel: str
    """全部加選方式"""
    page_cnt: int
    """頁數"""
    startrec: int
    """起始紀錄"""


MAX_PAGE_COUNT = 150


def _build_params(
    offset: int,
    params: QuickQueryParams,
) -> Params:
    query_page_count = params.get("query_page_count", MAX_PAGE_COUNT)
    if query_page_count > MAX_PAGE_COUNT:
        raise ValueError(f"page_count must be less than {MAX_PAGE_COUNT}")

    return {
        "current_sem": params.get("semester", get_current_semester()),
        "cstype": params["type"].value,
        "csname": params["keyword"],
        "alltime": "yes",
        "allproced": "yes",
        "allsel": "yes",
        "page_cnt": query_page_count,
        "startrec": offset,
    }


class QuickQueryParams(QueryParams):
    type: QueryType
    keyword: str


class QuickQuerySender(QuerySender[QuickQueryParams]):
    """
    A paginated search result.
    """

    @property
    def url_path(self) -> str:
        return "/search_result.php"

    @override
    async def get_total(self) -> int:
        params: Params = _build_params(0, self.params)
        # response = await self.client.get(self.url_path, params=to_str_dict(params))
        # print(params)
        # response =await self._query_page(0)
        # response = httpx.Client().send(self.client.build_request("GET", self.url_path, params=to_str_dict(params)))
        response = await httpx.AsyncClient().send(
            self.client.build_request("GET", self.url_path, params=to_str_dict(params))
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return int(soup.select("table")[5].select("td b")[0].text)

    @override
    async def _query_page(self, query_page_idx: int) -> httpx.Response:
        logger.info(f"Querying page {query_page_idx}")

        params: Params = _build_params(
            query_page_idx * self.params.get("query_page_count", MAX_PAGE_COUNT),
            self.params,
        )

        response = await self.client.get(
            self.url_path,
            params=to_str_dict(params),
        )

        logger.info(f"Finished querying page {query_page_idx}")

        response.raise_for_status()
        return response
