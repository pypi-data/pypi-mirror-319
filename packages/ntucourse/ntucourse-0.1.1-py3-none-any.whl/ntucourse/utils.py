import asyncio
import functools
import inspect
import logging
import traceback
from pathlib import Path
from typing import Callable, Concatenate, Mapping

from bs4 import BeautifulSoup
from loguru import logger


def async_lru_cache[**P, R](
    maxsize: int | None = 128,
    typed: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def async_lru_cache_decorator(async_function: Callable[P, R]) -> Callable[P, R]:
        @functools.lru_cache(maxsize, typed)
        def cached_async_function(*args: P.args, **kwargs: P.kwargs) -> R:
            coroutine = async_function(*args, **kwargs)
            return asyncio.ensure_future(coroutine)  # pyright: ignore

        return cached_async_function  # pyright: ignore

    return async_lru_cache_decorator


def to_str_dict(d: Mapping[str, object]) -> dict[str, str]:
    return {k: str(v) for k, v in d.items()}


def get_current_semester() -> str:
    return "113-2"


def truncate(s: str, max_length: int = 100) -> str:
    if len(s) > max_length:
        return s[:max_length] + "..."
    return s


def truncate_args(args: tuple[object, ...]) -> str:
    return ", ".join(truncate(str(arg)) for arg in args[:10])


def truncate_kwargs(kwargs: dict[str, object]) -> str:
    return ", ".join(f"{k}={truncate(str(v))}" for k, v in kwargs.items())


def record_error[**P, R](
    *,
    error_type: type[Exception] = Exception,
    return_func: Callable[Concatenate[Exception, P], R] | R | None = None,
    record_name: str | None = None,
    record_suffix: str = "",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler("debug.log"))

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return await func(*args, **kwargs)  # pyright: ignore
            except error_type as e:
                if record_name is not None:
                    names = record_name.split(".")
                else:
                    names = []

                truncated_args = truncate_args(args)
                truncated_kwargs = truncate_kwargs(kwargs)
                logger.error(f"{func.__name__} failed: {e}; Args: {truncated_args}; Kwargs: {truncated_kwargs}")

                tb = e.__traceback__
                if tb and tb.tb_next:
                    frame = tb.tb_next.tb_frame
                    if names and names[0] in frame.f_locals:
                        v = frame.f_locals[names[0]]
                        for name in names[1:]:
                            if v is None:
                                break
                            v = getattr(v, name, None)
                        if v is not None:
                            output_dir = Path("debug") / func.__name__
                            output_dir.mkdir(parents=True, exist_ok=True)
                            cnt = len(list(output_dir.glob(f"*{record_suffix}")))
                            with open(output_dir / f"{record_name}.{cnt}{record_suffix}", "w") as f:
                                f.write(str(v))
                    # breakpoint()

                if callable(return_func):
                    return return_func(e, *args, **kwargs)  # pyright: ignore
                return None  # pyright: ignore

        return wrapper  # pyright: ignore

    return decorator


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")
