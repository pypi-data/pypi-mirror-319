from __future__ import annotations

import asyncio
from abc import abstractmethod
from asyncio import iscoroutinefunction
from collections import defaultdict
from contextlib import nullcontext
from functools import wraps
from itertools import pairwise
from typing import (
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Callable,
    Concatenate,
    Protocol,
    Sequence,
    Sized,
    final,
    overload,
)

from loguru import logger


class AsyncSequence[T](Sized, AsyncIterable[T], Protocol):
    @abstractmethod
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> Awaitable[T]: ...

    @overload
    def __getitem__(self, index: slice) -> Awaitable[Sequence[T]]: ...

    @abstractmethod
    def __getitem__(self, index: int | slice) -> Awaitable[T] | Awaitable[Sequence[T]]:
        raise IndexError

    async def __aiter__(self) -> AsyncGenerator[T, None]:
        i = 0
        try:
            while True:
                v = await self[i]
                yield v
                i += 1
        except IndexError:
            return

    async def __contains__(self, value: object) -> bool:
        async for v in self:
            if v is value or v == value:
                return True
        return False

    async def __reversed__(self) -> AsyncGenerator[T, None]:
        for i in reversed(range(len(self))):
            yield await self[i]

    async def index(self, value: object, start: int = 0, stop: int | None = None) -> int:
        if start < 0:
            start = max(len(self) + start, 0)
        if stop is not None and stop < 0:
            stop += len(self)

        i = start
        while stop is None or i < stop:
            try:
                v = self[i]
            except IndexError:
                break
            if v is value or v == value:
                return i
            i += 1
        raise ValueError

    async def count(self, value: object):
        return sum(1 for v in self if v is value or v == value)


def _process_slice(slice: slice, total: int) -> tuple[int, int, int]:
    if any(x is not None and not isinstance(x, int) for x in (slice.start, slice.stop, slice.step)):
        raise ValueError("Slice must be an integer or None")

    start = slice.start
    if start is None:
        start = 0
    elif start < 0:
        start += total

    stop = slice.stop
    if stop is None:
        stop = total
    elif stop < 0:
        stop += total

    step = slice.step
    if step is None:
        step = 1

    return start, stop, step


# todo
MAX_BATCH_SIZE = 5


class ProgressCallback[T](Protocol):
    def __call__(self, idx: int, item: T) -> None: ...


class PaginationObserver[T](Protocol):
    @abstractmethod
    def on_getitem(self, index: int | slice, item_count: int) -> None: ...

    @abstractmethod
    def on_item_loaded(self, index: int, item: T) -> None: ...

    @abstractmethod
    def on_items_loaded(self, indices: list[int], items: list[T]) -> None: ...


# TODO: should we do lazy object validation?
class AsyncPaginatedList[T](AsyncSequence[T], Protocol):
    # --------------------------------- Abstract --------------------------------- #

    @abstractmethod
    async def _fetch_total(self) -> int: ...

    @abstractmethod
    async def _load_pages(
        self, page_indices: list[int], on_progress: ProgressCallback[T] | None = None
    ) -> list[list[T]]: ...

    # -------------------------------- Parameters -------------------------------- #

    # todo: _page_size is None
    _page_size: int
    _page_batch_size: int
    _concurrency: int

    # ----------------------------------- State ---------------------------------- #
    _total: int
    _pages: list[list[T] | None]
    _batch_loaded: set[int]
    _observer: PaginationObserver[T] | None

    def __init__(
        self, page_size: int, page_batch_size: int, concurrency: int, observer: PaginationObserver[T] | None = None
    ):
        self._total = -1
        self._page_size = page_size
        self._page_batch_size = page_batch_size
        self._concurrency = concurrency
        self._pages = []
        self._batch_loaded = set()
        self._observer = observer

    @property
    def _total_set(self) -> bool:
        return self._total != -1

    async def _init_total(self) -> int:
        self._total = await self._fetch_total()
        self._pages = [None] * self.page_count
        return self._total

    @staticmethod
    def init_required[**P, R](
        method: Callable[Concatenate[AsyncPaginatedList[T], P], R],
    ) -> Callable[Concatenate[AsyncPaginatedList[T], P], R]:
        if iscoroutinefunction(method):

            @wraps(method)
            async def async_wrapper(self: AsyncPaginatedList[T], *args: P.args, **kwargs: P.kwargs) -> R:
                if not self._total_set:
                    self._total = await self._init_total()
                return await method(self, *args, **kwargs)

            return async_wrapper  # pyright: ignore

        @wraps(method)
        def wrapper(self: AsyncPaginatedList[T], *args: P.args, **kwargs: P.kwargs) -> R:
            if not self._total_set:
                raise ValueError("Total is not set")
            return method(self, *args, **kwargs)

        return wrapper

    @property
    @init_required
    def total(self) -> int:
        return self._total

    @property
    @init_required
    def pages(self) -> list[list[T] | None]:
        return self._pages

    @property
    def page_count(self) -> int:
        return (self.total + self._page_size - 1) // self._page_size

    def _get_page(self, page_index: int) -> list[T] | None:
        return self.pages[page_index]

    def _set_page(self, page_index: int, page: list[T]) -> None:
        assert len(page) == self._calculate_page_size(
            page_index
        ), f"page size mismatch: {len(page)} != {self._calculate_page_size(page_index)}"
        self.pages[page_index] = page

    def _get(self, index: int) -> T:
        """Faster access to the element at index assuming the element is already loaded"""
        page_index, offset = self._calculate_offsets(index)
        page = self._get_page(page_index)
        assert page is not None
        assert len(page) == self._calculate_page_size(
            page_index
        ), f"page size mismatch: {len(page)} != {self._calculate_page_size(page_index)}"
        return page[offset]

    @final
    def _calculate_offsets(self, index: int) -> tuple[int, int]:
        if index < 0:
            index += self._total
        if index < 0:
            raise IndexError("Index out of bounds")
        return index // self._page_size, index % self._page_size

    @final
    def _calculate_page_idxs(self, page_index: int) -> list[int]:
        return list(range(page_index * self._page_size, (page_index + 1) * self._page_size))

    @final
    def _calculate_page_size(self, page_index: int) -> int:
        return min(self._page_size, self._total - page_index * self._page_size)

    @final
    def _calculate_batch_idx(self, page_index: int) -> int:
        return page_index // self._page_batch_size

    @property
    def _batch_page_indices(self) -> list[list[int]]:
        return [
            list(range(i, j)) for i, j in pairwise((*range(0, self.page_count, self._page_batch_size), self.page_count))
        ]

    def _get_batchs(self, page_indices: list[int]) -> list[list[int]]:
        batch_idxs = set[int]()
        for i in set(page_indices):
            batch_idxs.add(self._calculate_batch_idx(i))
        return [self._batch_page_indices[i] for i in batch_idxs]

    def _is_page_loaded(self, page_idx: int) -> bool:
        return self._calculate_batch_idx(page_idx) in self._batch_loaded

    def _on_item_loaded(self, idx: int, item: T) -> None:
        if self._observer:
            self._observer.on_item_loaded(idx, item)

    def _on_items_loaded(self, idxs: list[int], items: list[T]) -> None:
        if self._observer:
            self._observer.on_items_loaded(idxs, items)

    async def _get_slice(self, slice: slice) -> Sequence[T]:
        # todo: generator?
        start, stop, step = _process_slice(slice, self._total)
        getitems = lambda idxs: [self._get(i) for i in idxs]  # noqa: E731

        slice_idxs = range(start, stop, step)
        page_idxs = [self._calculate_offsets(i)[0] for i in range(start, stop, step)]
        slice_to_page = dict(zip(slice_idxs, page_idxs))
        page_to_slices = defaultdict(list)
        for i, page_idx in slice_to_page.items():
            page_to_slices[page_idx].append(i)

        pre_loaded_batch_idxs = {i for i, page_idx in zip(slice_idxs, page_idxs) if self._is_page_loaded(page_idx)}
        if self._observer:
            self._observer.on_getitem(slice, len(slice_idxs))
            # Trigger observer on pre-loaded items
            self._observer.on_items_loaded(list(pre_loaded_batch_idxs), getitems(pre_loaded_batch_idxs))

        logger.info(f"Total slice: {len(slice_idxs)}")
        logger.info(f"Need to load: {len(slice_idxs) - len(pre_loaded_batch_idxs)}")
        logger.info(f"Pages: {page_idxs}")

        # lock = asyncio.Semaphore(self._concurrency)
        # lock = asyncio.Semaphore(100000)

        def on_progress(idx: int, item: T) -> None:
            if idx in slice_idxs:
                self._on_item_loaded(idx, item)

        async def load_pages(page_idxs: list[int]) -> None:
            # async with lock:
            async with nullcontext():
                pages = await self._load_pages(page_idxs, on_progress)
                for page_idx, page in zip(page_idxs, pages):
                    self._set_page(page_idx, page)

        # ? Sequential or pooling

        tasks: list[Awaitable[None]] = []
        batch_page_idxs = self._get_batchs(page_idxs)
        for page_idxs in batch_page_idxs:
            _batch_idxs = {self._calculate_batch_idx(i) for i in page_idxs}
            assert len(_batch_idxs) == 1, "Should be a single batch"
            batch_idx = _batch_idxs.pop()

            if not self._is_page_loaded(batch_idx):
                tasks.append(load_pages(page_idxs))

        await asyncio.gather(*tasks)

        # lock = asyncio.Semaphore(5)

        # async def task(i: int):
        #     async with lock:
        #         return await self._load_pages([i])

        # await asyncio.gather(*[task(i) for i in range(20)])

        # return []
        # await asyncio.gather(*tasks)

        # Trigger observer on newly loaded items
        # for i in slice_idxs:
        #     if self._observer and i not in pre_loaded_batch_idxs:
        #         self._observer.on_item_loaded(i, self._get(i))

        return getitems(slice_idxs)

    @overload
    async def __getitem__(self, index: int) -> T: ...

    @overload
    async def __getitem__(self, index: slice) -> Sequence[T]: ...

    @init_required
    async def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        logger.info(f"Getting item {index}")

        assert isinstance(index, (int, slice))
        if isinstance(index, int):
            if self._observer:
                self._observer.on_getitem(index, 1)

            page_index, offset = self._calculate_offsets(index)
            if (page := self.pages[page_index]) is None:
                logger.info(f"Fetching page {page_index}")

                await self._load_pages([page_index])
                # self._set_page(page_index, page)
                page = self.pages[page_index]
                assert page is not None

            if self._observer:
                self._observer.on_item_loaded(index, page[offset])
            return page[offset]
        else:
            return await self._get_slice(index)

    def __len__(self) -> int:
        if not self._total_set:
            # todo
            raise ValueError("Total is not set")
        return self.total

    # @override
    # async def __aiter__(self) -> AsyncGenerator[T, None]:
    #     for i in range(self._page_count):
    #         page = await self._get_page(i)
    #         for element in page:
    #             yield element
