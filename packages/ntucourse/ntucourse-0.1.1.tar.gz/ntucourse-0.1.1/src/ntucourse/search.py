from __future__ import annotations

import asyncio
import typing
from typing import (
    Any,
    override,
)

import httpx
from loguru import logger
from pydantic import TypeAdapter

from .model import Course, Outline
from .paginated_list import AsyncPaginatedList, PaginationObserver, ProgressCallback
from .parse import parse_html, parse_outline
from .query_sender import MAX_PAGE_COUNT, QuerySender

if typing.TYPE_CHECKING:
    pass


class AsyncSearch(AsyncPaginatedList[Course]):
    """
    A paginated search result.
    """

    client: httpx.AsyncClient
    query_sender: QuerySender[Any]
    include_outline: bool

    _semaphore: asyncio.Semaphore

    def __init__(
        self,
        client: httpx.AsyncClient,
        query_sender: QuerySender[Any],
        page_batch_size: int,
        concurrency: int,
        include_outline: bool,
        observer: PaginationObserver[Course] | None = None,
    ):
        page_size = query_sender.query_page_count
        assert page_size <= MAX_PAGE_COUNT

        super().__init__(page_size, page_batch_size, 10000, observer)
        self._semaphore = asyncio.Semaphore(concurrency)
        self._outline_semaphore = asyncio.Semaphore(1000)
        self.client = client
        self.query_sender = query_sender
        self.include_outline = include_outline

    async def _update_course_outlines(
        self,
        page_idx: int,
        courses: list[Course],
        on_progress: ProgressCallback[Course] | None,
    ) -> list[Course]:
        async def task(course: Course) -> Course:
            index = self._calculate_page_idxs(page_idx)[courses.index(course)]
            if course.outline_url is None:
                if on_progress:
                    on_progress(index, course)
                return course

            logger.info(f"update course {index}")
            async with self._outline_semaphore:
                response = await self.client.get(course.outline_url)
            outline = parse_outline(response.text)
            course.outline = Outline(**outline) if outline else None
            logger.info(f"update course {index} end")

            if on_progress:
                on_progress(index, course)
            return course

        return await asyncio.gather(*[task(course) for course in courses])

    async def _parse_page(
        self,
        page_idx: int,
        response: httpx.Response,
        on_progress: ProgressCallback[Course] | None,
    ) -> list[Course]:
        parsed = parse_html(html=response.text, semester=self.query_sender.semester)
        courses = TypeAdapter(list[Course]).validate_python(parsed)

        if not self.include_outline:
            for i, course in enumerate(courses):
                index = self._calculate_page_idxs(page_idx)[i]
                if on_progress:
                    on_progress(index, course)
            return courses

        logger.info(f"update outline {page_idx}")
        await self._update_course_outlines(page_idx, courses, on_progress=on_progress)
        logger.info(f"update outline {page_idx} end")

        return courses

    @override
    async def _fetch_total(self) -> int:
        total = await self.query_sender.get_total()
        return total

    @override
    async def _load_pages(
        self,
        page_indices: list[int],
        on_progress: ProgressCallback[Course] | None = None,
    ):
        async with self._semaphore:
            # async with nullcontext():
            # print("load start", page_indices)
            pages = await self.query_sender.get_pages(page_indices)
            # print("load end", page_indices)

        res = await asyncio.gather(
            *[self._parse_page(page_idx, page, on_progress) for page_idx, page in zip(page_indices, pages)]
        )
        return res
