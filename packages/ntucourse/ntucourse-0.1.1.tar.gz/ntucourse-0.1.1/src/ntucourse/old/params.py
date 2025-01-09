from enum import Enum
from typing import (
    TypedDict,
)


class QueryType(Enum):
    TITLE = 1
    INSTRUCTOR = 2
    CODE = 3
    IDENTIFIER = 4
    SERIAL = 5


class Params(TypedDict):
    current_sem: str
    cstype: int
    csname: str
    alltime: str
    allproced: str
    allsel: str
    page_cnt: int
    start_rec: int


MAX_PAGE_COUNT = 150


def build_params(
    query_type: QueryType,
    query_value: str | int,
    semester: str,
    page_count: int,
    offset: int = 0,
) -> Params:
    if page_count > MAX_PAGE_COUNT:
        raise ValueError(f"page_count must be less than {MAX_PAGE_COUNT}")

    return {
        "current_sem": semester,
        "cstype": query_type.value,
        "csname": str(query_value),
        "alltime": "yes",
        "allproced": "yes",
        "allsel": "yes",
        "page_cnt": page_count,
        "start_rec": offset,
    }
