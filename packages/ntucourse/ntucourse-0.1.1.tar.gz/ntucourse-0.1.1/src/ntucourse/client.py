from __future__ import annotations

from types import TracebackType
from typing import IO, Any, Mapping, Self, TypedDict, Unpack

import httpx
from httpx._client import ClientState
from tqdm import tqdm

from .model import Course
from .paginated_list import PaginationObserver
from .query_sender import QuerySender
from .quick import QuickQueryParams, QuickQuerySender
from .search import AsyncSearch


class TqdmArgs(TypedDict, total=False):
    desc: str | None
    leave: bool | None
    file: IO[str] | None
    ncols: int | None
    mininterval: float
    maxinterval: float
    miniters: float | None
    ascii: bool | str | None
    disable: bool | None
    unit: str
    unit_scale: bool | float
    dynamic_ncols: bool
    smoothing: float
    bar_format: str | None
    initial: float
    position: int | None
    postfix: Mapping[str, object] | str | None
    unit_divisor: float
    write_bytes: bool
    lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None
    nrows: int | None
    colour: str | None
    delay: float | None
    gui: bool


class TqdmObserver(PaginationObserver[Course]):
    def __init__(self, args: TqdmArgs):
        self.args = args

    def on_getitem(self, index: int | slice, item_count: int) -> None:
        self.args.setdefault("leave", True)
        self.pbar = tqdm(total=item_count, **self.args)

    def on_item_loaded(self, index: int, item: Course) -> None:
        self.pbar.update(1)
        if self.pbar.n == self.pbar.total:
            self.pbar.close()

    def on_items_loaded(self, indices: list[int], items: list[Course]) -> None:
        self.pbar.update(len(items))
        if self.pbar.n == self.pbar.total:
            self.pbar.close()


class AsyncClient:
    httpx_client: httpx.AsyncClient

    _own_httpx_client: bool

    def __init__(self, *, httpx_client: httpx.AsyncClient | None = None):
        self.httpx_client = httpx_client or httpx.AsyncClient(
            timeout=httpx.Timeout(20),
            limits=httpx.Limits(max_connections=100),
        )
        self.httpx_client.base_url = "https://nol.ntu.edu.tw/nol/coursesearch"
        self._own_httpx_client = httpx_client is None

    async def __aenter__(self) -> Self:
        if self.httpx_client._state == ClientState.UNOPENED:
            await self.httpx_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._own_httpx_client:
            await self.httpx_client.__aexit__(exc_type, exc_value, traceback)

    # @overload
    # def search_quick(
    #     self,
    #     *,
    #     page_batch_size: int = ...,
    #     tqdm: Literal[True] | TqdmArgs = True,
    #     **kwargs: Unpack[QuickQueryParams],
    # ) -> AsyncSearch: ...

    # @overload
    # def search_quick(
    #     self,
    #     *,
    #     page_batch_size: int = ...,
    #     tqdm: Literal[False] = False,
    #     observer: PaginationObserver[Course] | None = None,
    #     **kwargs: Unpack[QuickQueryParams],
    # ) -> AsyncSearch: ...

    def search_quick(
        self,
        *,
        page_batch_size: int = 1,
        concurrency: int = 10,
        tqdm: bool | TqdmArgs = True,
        observer: PaginationObserver[Course] | None = None,
        include_outline: bool = False,
        **kwargs: Unpack[QuickQueryParams],
    ) -> AsyncSearch:
        query_sender = QuickQuerySender(kwargs, self.httpx_client)
        if tqdm:
            if tqdm is True:
                tqdm = {}
            observer = TqdmObserver(tqdm)

        return self._search(query_sender, page_batch_size, concurrency, observer, include_outline)

    def _search(
        self,
        query_sender: QuerySender[Any],
        page_batch_size: int,
        concurrency: int,
        observer: PaginationObserver[Course] | None,
        include_outline: bool,
    ) -> AsyncSearch:
        return AsyncSearch(
            self.httpx_client,
            query_sender,
            page_batch_size=page_batch_size,
            concurrency=concurrency,
            observer=observer,
            include_outline=include_outline,
        )
