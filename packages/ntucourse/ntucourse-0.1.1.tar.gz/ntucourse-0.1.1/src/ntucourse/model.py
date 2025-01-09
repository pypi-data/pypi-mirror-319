from enum import Enum
from typing import Annotated, Any, Callable

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    ValidationError,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)

# TODO: strict mode

def fallback_validator[T](
    default: Callable[[], T] | T,
) -> WrapValidator:
    def validator(value: Any, handler: ValidatorFunctionWrapHandler) -> T:
        try:
            return handler(value)
        except ValidationError:
            if callable(default):
                return default()  # pyright: ignore
            return default

    return WrapValidator(validator)


def nullify_empty_str(value: str) -> str | None:
    if value == "":
        return None
    return value


class Duration(Enum):
    FULL = "全年"
    HALF = "半年"


class Category(Enum):
    REQUIRED = "必修"
    AUTO_ENROLLED = "必帶"
    ELECTIVE = "選修"


class EnrollmentRule(Enum):
    OPEN = 1
    APPROVAL = 2
    ALLOCATION = 3


class Outline(BaseModel):
    overview: str = Field(
        description="課程概述",
        serialization_alias="課程概述",
    )
    goal: str = Field(description="課程目標", serialization_alias="課程目標")
    requirement: str = Field(description="課程要求", serialization_alias="課程要求")
    expected_study_hours: str = Field(description="預期每週課後學習時數", serialization_alias="預期每週課後學習時數")
    office_hours: str = Field(description="Office Hours", serialization_alias="Office Hours")
    reading: str = Field(description="指定閱讀", serialization_alias="指定閱讀")
    reference: str = Field(description="參考書目", serialization_alias="參考書目")
    evaluation: str = Field(description="評量方式", serialization_alias="評量方式")


class Instructor(BaseModel):
    name: str = Field(description="姓名", serialization_alias="姓名")
    department: str = Field(description="所屬系所", serialization_alias="所屬系所")
    title: str = Field(description="職稱", serialization_alias="職稱")
    homepage: str | None = Field(description="個人首頁網址", default=None, serialization_alias="個人首頁網址")
    email: str | None = Field(description="E-Mail地址", default=None, serialization_alias="E-Mail地址")
    phone: str | None = Field(description="聯絡電話", default=None, serialization_alias="聯絡電話")
    office: str | None = Field(description="辦公室", default=None, serialization_alias="辦公室")
    personal_info: str | None = Field(description="個人資訊", default=None, serialization_alias="個人資訊")


class Classroom(BaseModel):
    uid: str
    name: str
    url: str | None = Field(description="教室網頁", default=None)


class Schedule(BaseModel):
    day: int  # 0-6
    start: int
    end: int
    classroom: Classroom


def truncate(value: Any, handler: ValidatorFunctionWrapHandler) -> str:
    try:
        return handler(value)
    except ValidationError as err:
        if err.errors()[0]["type"] == "string_too_long":
            return handler(value[:5])
        else:
            raise


class Course(BaseModel):
    serial: str | None = Field(description="流水號", serialization_alias="流水號", examples=["38273", "12345"])
    department: str = Field(
        default="",
        description="授課對象",
        serialization_alias="授課對象",
        examples=["資訊工程學系", "理學院  物理學系", "資工系"],
    )
    code: str = Field(
        description="課號",
        serialization_alias="課號",
        examples=["CSIE1212", "Phys2020", "MATH1001"],
    )
    class_id: str = Field(description="班次", serialization_alias="班次", examples=["01", "02", ""])
    title: str = Field(
        description="課程名稱",
        serialization_alias="課程名稱",
        examples=["資料結構與演算法", "電磁學下", "Data Structures and Algorithms"],
    )
    semester: str = Field(
        description="開課學期",
        serialization_alias="開課學期",
        examples=["113-2", "113-1"],
    )
    field_expertise: str = Field(
        description="領域專長",
        serialization_alias="領域專長",
        examples=["機器學習與人工智慧、自然語言處理", "電磁學、物理"],
    )
    credits: float = Field(description="學分", serialization_alias="學分", examples=[3.0, 2.0, 1.0])
    id: str = Field(
        description="課程識別碼",
        serialization_alias="課程識別碼",
        examples=["902 10750", "202 23302"],
    )
    duration: Annotated[Duration | None, BeforeValidator(nullify_empty_str)] = Field(
        description="全/半年",
        serialization_alias="全/半年",
        examples=[Duration.HALF, Duration.FULL],
    )
    category: Annotated[Category | None, BeforeValidator(nullify_empty_str)] = Field(
        description="必/選修",
        serialization_alias="必/選修",
        examples=[Category.AUTO_ENROLLED, Category.REQUIRED, Category.ELECTIVE],
    )
    instructor_str: Annotated[str | None, BeforeValidator(nullify_empty_str)] = Field(
        description="授課教師",
        serialization_alias="授課教師",
        examples=["林軒田"],
    )
    instructor: Annotated[Instructor | None, fallback_validator(None)] = Field(
        default=None,
        description="授課教師",
        serialization_alias="授課教師",
    )
    enrollment_rule: Annotated[EnrollmentRule | None, BeforeValidator(nullify_empty_str), fallback_validator(None)] = (
        Field(
            description="加選方式",
            serialization_alias="加選方式",
            examples=[
                EnrollmentRule.APPROVAL,
                EnrollmentRule.OPEN,
                EnrollmentRule.ALLOCATION,
            ],
        )
    )
    schedule_str: str = Field(
        description="時間教室",
        serialization_alias="時間教室",
        examples=["二6,7,8(請洽系所辦)", "星期二6,7,8(13:20~16:20)"],
    )
    schedules: list[Schedule] = Field(
        default=[],
        description="時間教室",
        exclude=True,
    )
    max_students: Annotated[int | None, BeforeValidator(nullify_empty_str)] = Field(
        description="總人數", serialization_alias="總人數", examples=[100, 50, 200]
    )
    restrictions: str = Field(
        description="選課限制條件",
        serialization_alias="選課限制條件",
        examples=[
            "限本系所學生(含輔系、雙修生) 且 限學號單號,本校修課人數上限：240人",
        ],
    )
    remarks: str = Field(
        description="備註",
        serialization_alias="備註",
        examples=[
            "主播教室：資103。資102、資104同步與蔡欣穆合授",
            "本課程中文授課,使用英文教科書。",
        ],
    )
    website: str | None = Field(
        description="課程網頁",
        default=None,
        serialization_alias="課程網頁",
        examples=[None, "https://cool.ntu.edu.tw/courses/12345"],
    )
    outline_url: str | None = Field(
        description="課程大綱網頁",
        default=None,
        serialization_alias="課程大綱網頁",
        examples=[None, "https://cool.ntu.edu.tw/courses/12345"],
    )
    outline: Outline | None = Field(
        description="課程大綱",
        serialization_alias="課程大綱",
        default=None,
    )
