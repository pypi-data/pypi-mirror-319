from __future__ import annotations

import enum
import typing as t
import uuid
from dataclasses import KW_ONLY, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import uniserde
from uniserde import ObjectId


class RegularEnum(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class FlagEnum(enum.Flag):
    ONE = 1
    TWO = 2
    FOUR = 4


@dataclass
class SimpleClass(uniserde.Serde):
    foo: int
    bar: str


@dataclass
class TestClass(uniserde.Serde):
    val_bool: bool
    val_int: int
    val_float: float
    val_bytes: bytes
    val_str: str
    val_datetime: datetime
    val_timedelta: timedelta
    val_tuple: tuple[int, str]
    val_list: list[int]
    val_set: set[int]
    val_dict: dict[str, int]
    val_optional: t.Optional[int]
    val_old_union_optional_1: t.Union[int, None]
    val_old_union_optional_2: t.Union[None, int]
    val_new_union_optional_1: int | None
    val_new_union_optional_2: None | int
    val_any: t.Any
    val_object_id: ObjectId
    val_literal: t.Literal["one", "two", "three"]
    val_enum: RegularEnum
    val_flag: FlagEnum
    val_path: Path
    val_uuid: uuid.UUID

    @classmethod
    def create_variant_1(cls) -> "TestClass":
        return cls(
            val_bool=True,
            val_int=1,
            val_float=1.0,
            val_bytes=b"these are bytes",
            val_str="this is a string",
            val_datetime=datetime(2020, 1, 2, tzinfo=timezone.utc),
            val_timedelta=timedelta(days=1, seconds=2, microseconds=3),
            val_tuple=(1, "one"),
            val_list=[1, 2, 3],
            val_set={1, 2, 3},
            val_dict={"one": 1, "two": 2},
            val_optional=1,
            val_old_union_optional_1=1,
            val_old_union_optional_2=1,
            val_new_union_optional_1=1,
            val_new_union_optional_2=1,
            val_any="this is an ANY value",
            val_object_id=ObjectId("62bd611fa847c71f1b68fffb"),
            val_literal="one",
            val_enum=RegularEnum.ONE,
            val_flag=FlagEnum.ONE | FlagEnum.TWO,
            val_path=Path.home() / "one",
            val_uuid=uuid.UUID("754a5dbf-e7f3-4cc3-b2d7-9382e586cfd3"),
        )

    @classmethod
    def create_variant_2(cls) -> "TestClass":
        return cls(
            val_bool=False,
            val_int=2,
            val_float=2.0,
            val_bytes=b"these are different bytes",
            val_str="this is another string",
            val_datetime=datetime(2024, 5, 6, tzinfo=timezone.utc),
            val_timedelta=timedelta(days=10, seconds=20, microseconds=30),
            val_tuple=(2, "two"),
            val_list=[4, 5, 6],
            val_set={4, 5, 6},
            val_dict={"three": 3, "four": 4},
            val_optional=None,
            val_old_union_optional_1=None,
            val_old_union_optional_2=None,
            val_new_union_optional_1=None,
            val_new_union_optional_2=None,
            val_any="this is another ANY value",
            val_object_id=ObjectId("62bd6122a847c71f1b68fffc"),
            val_literal="two",
            val_enum=RegularEnum.TWO,
            val_flag=FlagEnum.ONE | FlagEnum.TWO | FlagEnum.FOUR,
            val_path=Path.home() / "two",
            val_uuid=uuid.UUID("0eadbc7e-3418-45a5-b276-53e7d91bb79d"),
        )


@dataclass
@uniserde.as_child
class ParentClass(uniserde.Serde):
    parent_int: int
    parent_float: float

    @classmethod
    def create_parent_variant_1(cls) -> "ParentClass":
        return cls(
            parent_int=1,
            parent_float=1.0,
        )


@dataclass
class ChildClass(ParentClass):
    child_float: float
    child_str: str

    @classmethod
    def create_child_variant_1(cls) -> "ChildClass":
        return cls(
            parent_int=1,
            parent_float=1.0,
            child_float=1.0,
            child_str="this is a string",
        )


@dataclass
class ClassWithId(uniserde.Serde):
    id: int
    foo: int

    @classmethod
    def create(cls) -> "ClassWithId":
        return cls(1, 2)


@dataclass
class ClassWithKwOnly(uniserde.Serde):
    foo: int

    _: KW_ONLY

    bar: int

    @classmethod
    def create(cls) -> "ClassWithKwOnly":
        return cls(1, bar=2)


@dataclass
class ClassWithStaticmethodOverrides(uniserde.Serde):
    """
    Class which has uniserde's special methods overridden. This allows to check
    that they are called rather than the default.

    All methods are overridden as @staticmethod.
    """

    value: str
    format: str

    @classmethod
    def create(cls) -> "ClassWithStaticmethodOverrides":
        return cls("stored value", "python")

    def as_json(
        self,
        *,
        as_type: t.Optional[t.Type] = None,
        custom_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> uniserde.JsonDoc:
        return {"value": "overridden value", "format": "json"}

    def as_bson(
        self,
        *,
        as_type: t.Optional[t.Type] = None,
        custom_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> uniserde.BsonDoc:
        return {"value": "overridden value", "format": "bson"}

    @staticmethod
    def from_json(
        document: dict[str, t.Any],
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> "ClassWithStaticmethodOverrides":
        return ClassWithStaticmethodOverrides("overridden value", "json")

    @staticmethod
    def from_bson(
        document: dict[str, t.Any],
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> "ClassWithStaticmethodOverrides":
        return ClassWithStaticmethodOverrides("overridden value", "bson")

    @staticmethod
    def as_mongodb_schema(
        custom_handlers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> t.Any:
        return {"value": "overridden value", "format": "mongodb schema"}


@dataclass
class ClassWithClassmethodOverrides(uniserde.Serde):
    """
    Same as the class above, but with the methods overridden as @classmethod.
    """

    value: str
    format: str

    @classmethod
    def create(cls) -> "ClassWithClassmethodOverrides":
        return cls("stored value", "python")

    @classmethod
    def from_json(
        cls,
        document: dict[str, t.Any],
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> "ClassWithClassmethodOverrides":
        return ClassWithClassmethodOverrides("overridden value", "json")

    @classmethod
    def from_bson(
        cls,
        document: dict[str, t.Any],
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> "ClassWithClassmethodOverrides":
        return ClassWithClassmethodOverrides("overridden value", "bson")

    @classmethod
    def as_mongodb_schema(
        cls,
        custom_handlers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> t.Any:
        return {"value": "overridden value", "format": "mongodb schema"}
