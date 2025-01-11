from __future__ import annotations

import base64
import enum
import inspect
import typing
import typing as t
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from . import case_convert, common, serde_class
from .common import *
from .common import Recur, Serializer, common_serialize
from .objectid_proxy import ObjectId
from .typedefs import JsonDoc

__all__ = [
    "as_json",
]


def serialize_bool_to_bool(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> bool:
    assert isinstance(value, bool), value
    return value


def serialize_int_to_int(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> int:
    assert isinstance(value, int), value
    return value


def serialize_float_to_float(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> float:
    assert isinstance(value, (int, float)), value
    return float(value)


def serialize_bytes_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, bytes), value
    return base64.b64encode(value).decode("utf-8")


def serialize_str_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, str), value
    return value


def serialize_datetime_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, datetime), value
    assert (
        value.tzinfo is not None
    ), f"Encountered datetime without a timezone. Please always set timezones, or expect hard to find bugs."
    return value.isoformat()


def serialize_timedelta_to_float(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> float:
    assert isinstance(value, timedelta), value
    return value.total_seconds()


def serialize_tuple_as_list(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> list[t.Any]:
    assert isinstance(value, tuple), value
    subtypes = typing.get_args(value_type)
    assert len(subtypes) == len(value), (subtypes, value)

    return [recur(v, subtype) for v, subtype in zip(value, subtypes)]


def serialize_list_to_list(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> list[t.Any]:
    assert isinstance(value, list), value
    return [recur(v, typing.get_args(value_type)[0]) for v in value]


def serialize_set_as_list(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> list[t.Any]:
    assert isinstance(value, set), value
    subtype = typing.get_args(value_type)[0]
    return [recur(v, subtype) for v in value]


def serialize_dict_to_dict(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> dict[t.Any, t.Any]:
    subtypes = typing.get_args(value_type)
    assert isinstance(value, dict), value
    return {recur(k, subtypes[0]): recur(v, subtypes[1]) for k, v in value.items()}


def serialize_object_id_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, ObjectId), value
    return str(value)


def serialize_optional(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> t.Any:
    if value is None:
        return None

    for subtype in typing.get_args(value_type):
        if subtype is not type(None):
            break
    else:
        assert False, "No `None` in an `Optional` type?"

    return recur(value, subtype)


def serialize_any(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> t.Any:
    return value


def serialize_literal_as_is(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> t.Any:
    assert isinstance(value, str), value
    return value


def serialize_path_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, Path), value
    return str(value.absolute())


def serialize_uuid_to_str(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> str:
    assert isinstance(value, uuid.UUID), value
    return str(value)


def serialize_class(
    value: t.Any,
    value_type: t.Type,
    recur: Recur,
) -> t.Any:
    assert inspect.isclass(value_type), value_type

    # Case: The class has a custom serialization method
    try:
        override_method = getattr(value, "as_json")
    except AttributeError:
        pass
    else:
        if override_method.__func__ is not serde_class.Serde.as_json:
            return override_method()

    # Case: enum.Flag
    if issubclass(value_type, enum.Flag):
        assert isinstance(value, value_type), value
        return [case_convert.all_upper_to_camel_case(flag.name) for flag in value]  # type: ignore

    # Case: enum.Enum
    if issubclass(value_type, enum.Enum):
        assert isinstance(value, value_type), value
        return case_convert.all_upper_to_camel_case(value.name)

    # Case: t.Anything else
    # Make sure to serialize as the correct class
    if common.should_serialize_as_child(value_type):
        assert issubclass(type(value), value_type), (type(value), value_type)
        value_type = type(value)

    result = {}
    for field_py_name, field_type in common.custom_get_type_hints(value_type).items():
        field_doc_name = case_convert.all_lower_to_camel_case(field_py_name)
        result[field_doc_name] = recur(getattr(value, field_py_name), field_type)

    # Add a type tag?
    if common.should_serialize_as_child(value_type):
        result["type"] = case_convert.upper_camel_case_to_camel_case(
            value.__class__.__name__
        )

    return result


JSON_SERIALIZERS: dict[t.Type, Serializer] = {
    bool: serialize_bool_to_bool,
    int: serialize_int_to_int,
    float: serialize_float_to_float,
    bytes: serialize_bytes_to_str,
    str: serialize_str_to_str,
    datetime: serialize_datetime_to_str,
    timedelta: serialize_timedelta_to_float,
    tuple: serialize_tuple_as_list,
    list: serialize_list_to_list,
    set: serialize_set_as_list,
    dict: serialize_dict_to_dict,
    t.Union: serialize_optional,
    t.Any: serialize_any,
    ObjectId: serialize_object_id_to_str,
    t.Literal: serialize_literal_as_is,
    Path: serialize_path_to_str,
    type(Path()): serialize_path_to_str,
    uuid.UUID: serialize_uuid_to_str,
}


def as_json(
    value: t.Any,
    *,
    as_type: t.Optional[t.Type] = None,
    custom_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
) -> JsonDoc:
    return common_serialize(
        value,
        type(value) if as_type is None else as_type,
        serialize_class,
        JSON_SERIALIZERS,
        custom_serializers,
    )
