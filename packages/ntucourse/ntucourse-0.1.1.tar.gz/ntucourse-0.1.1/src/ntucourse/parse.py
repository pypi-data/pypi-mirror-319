import re
from typing import Any, Literal, cast

from bs4 import NavigableString, ResultSet, Tag
from loguru import logger

from .utils import get_soup


def get_label_name(td: Tag) -> str:
    return "".join(map(str, filter(lambda x: isinstance(x, NavigableString), td.contents)))


# class CourseDict(TypedDict):
#     serial: str
#     department: str
#     code: str
#     class_id: str
#     title: str
#     semester: str
#     field_expertise: str
#     credits: float
#     id: str
#     duration: str
#     category: str
#     instructor: dict[str, str | None]
#     enrollment_rule: int
#     schedule_str: str
#     schedules: list[dict[str, str | int]]
#     max_students: int
#     restrictions: str
#     remarks: str
#     website: str | None
#     outline: dict[str, str]


def get_tag_text(tag: Tag) -> str:
    return tag.text.strip().replace("\n", " ").replace("<br>", "\n")


Label = Literal[
    "serial",
    "department",
    "code",
    "class_id",
    "title",
    "field_expertise",
    "credits",
    "id",
    "duration",
    "category",
    "instructor_str",
    "enrollment_rule",
    "schedule_str",
    "max_students",
    "restrictions",
    "remarks",
    "website",
]

LABEL_LOOKUP: dict[str, Label | None] = {
    "流水號": "serial",
    "授課對象": "department",
    "課號": "code",
    "班次": "class_id",
    "課程名稱": "title",
    "領域專長": "field_expertise",
    "學分": "credits",
    "課程識別碼": "id",
    "全/半年": "duration",
    "必/選修": "category",
    "授課教師": "instructor_str",
    "加選方式": "enrollment_rule",
    "時間教室": "schedule_str",
    "總人數": "max_students",
    "選課限制條件": "restrictions",
    "備註": "remarks",
    "課程網頁": "website",
}


@logger.catch
def parse_label_tag(tag: Tag, label: Label):
    text = tag.text.strip()
    match label:
        case "serial":
            return text
        case "department":
            return text
        case "code":
            return text
        case "class_id":
            return text
        case "title":
            return text
        case "field_expertise":
            return text
        case "credits":
            return text
        case "id":
            return text
        case "duration":
            return text
        case "category":
            return text
        case "instructor_str":
            return text
        case "enrollment_rule":
            return text
        case "schedule_str":
            return text
        case "max_students":
            return re.sub(r"\(.*?\)", "", text)
        case "restrictions":
            return text
        case "remarks":
            return text
        case "website":
            return text

    raise TypeError(f"Unknown label: {label}")  # pyright: ignore


@logger.catch
def get_outline_url(tag: Tag) -> str | None:
    try:
        return cast(str, tag.select("a")[0]["href"])
    except IndexError:
        return None


def parse_html(html: str, semester: str) -> list[dict[str, Any]]:
    soup = get_soup(html)
    table = soup.select("table")[6]
    rows: ResultSet[Tag] = table.select("tr")

    # drop "本學期我預計要選的課程"
    column_labels = [get_label_name(td) for td in rows[0].select("td")][:-1]
    assert len(column_labels) == len(LABEL_LOOKUP), f"{column_labels} != {LABEL_LOOKUP}"
    for label in column_labels:
        if label not in LABEL_LOOKUP:
            raise ValueError(f"Unknown label: {label}")

    title_idx = 4
    assert column_labels[title_idx] == "課程名稱"

    courses: list[dict[str, Any]] = []
    for row in rows[1:]:
        tds = row.select("td")
        if not tds:  # Skip empty rows
            continue
        course_dict: dict[str, Any] = {}
        for label, td in zip(column_labels, tds):
            if (field_name := LABEL_LOOKUP[label]) is None:
                continue
            course_dict[field_name] = parse_label_tag(td, field_name)
        course_dict["semester"] = semester
        course_dict["outline_url"] = get_outline_url(tds[title_idx])

        courses.append(course_dict)
    return courses


type OutlineField = Literal[
    "overview",
    "goal",
    "requirement",
    "expected_study_hours",
    "office_hours",
    "reading",
    "reference",
    "evaluation",
]

OUTLINE_LOOKUP: dict[str, OutlineField] = {
    "課程概述": "overview",
    "課程目標": "goal",
    "課程要求": "requirement",
    "預期每週課後學習時數": "expected_study_hours",
    "Office Hours": "office_hours",
    "指定閱讀": "reading",
    "參考書目": "reference",
    "評量方式(僅供參考)": "evaluation",
}


def process_outline(field: OutlineField, tag: Tag) -> Any:
    text = tag.text.strip().replace("\r\n", " ").replace("\r", " ").replace("\n", " ").replace("<br>", "\n")
    match field:
        case _:
            return text


# @record_error(record_name="response.text", record_suffix=".html")
@logger.catch
def parse_outline(html: str) -> dict[str, str] | None:
    soup = get_soup(html)
    table = soup.select("table")[2]
    rows: ResultSet[Tag] = table.select("tr")

    outline_row_idx: int | None = None
    for i, row in enumerate(rows):
        if row.text.strip() == "課程大綱":
            outline_row_idx = i
            break

    if outline_row_idx is None:
        return None
    assert rows[outline_row_idx + 1].text.strip() == "為確保您我的權利,請尊重智慧財產權及不得非法影印"

    outline_dict: dict[str, str] = {}
    for row, (label, field) in zip(rows[outline_row_idx + 2 :], OUTLINE_LOOKUP.items()):
        assert row.select("td")[0].text.strip() == label, f"{row.text.strip()} != {label}"

        outline_dict[field] = process_outline(field, row.select("td")[1])

    return outline_dict


# todo
OVERWRITE_LOOKUP = {2: ("授課對象", "department")}
