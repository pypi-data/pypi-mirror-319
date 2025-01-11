from __future__ import annotations

import typing as t
from datetime import datetime, timezone

import typing_extensions as te

from . import caching_serdeserializer, case_convert, common, json_deserialize, typedefs
from .common import SerdeError
from .objectid_proxy import ObjectId

__all__ = [
    "from_bson",
]


T = te.TypeVar("T")


class BsonDeserializer(
    caching_serdeserializer.CachingSerDeserializer[typedefs.Bsonable, t.Any]
):
    def _get_class_fields(
        self, value_type: t.Type
    ) -> t.Iterable[tuple[str, str, t.Type]]:
        for field_name_py, field_type in common.custom_get_type_hints(
            value_type
        ).items():
            if field_name_py == "id":
                field_name_doc = "_id"
            else:
                field_name_doc = case_convert.all_lower_to_camel_case(field_name_py)

            yield (
                field_name_py,
                field_name_doc,
                field_type,
            )

    def _deserialize_datetime_from_datetime(
        self,
        value: typedefs.Bsonable,
        value_type: t.Type[datetime],
    ) -> datetime:
        if not isinstance(value, datetime):
            raise SerdeError(f"Expected datetime, got {value}")

        # BSON doesn't support timezones, and MongoDB convention dictates UTC to
        # be assumed. Impute that.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value

    _passthrough_types = {
        bool,
        int,
        float,
        bytes,
        str,
        ObjectId,
    }  # type: ignore

    _handler_cache = json_deserialize.JsonDeserializer._handler_cache.copy()  # type: ignore
    _handler_cache.update(
        {
            (True, datetime): _deserialize_datetime_from_datetime,
            (False, datetime): _deserialize_datetime_from_datetime,
        }  # type: ignore
    )

    _override_method_name = "from_bson"


def from_bson(
    document: t.Any,
    as_type: t.Type[T],
    *,
    custom_deserializers: dict[t.Type, t.Callable[[typedefs.Bsonable], t.Any]] = {},
    lazy: bool = False,
) -> T:
    """
    Deserialize an entire data class from BSON, by applying the field
    deserializer to each field. Field names are converted from camel case.

    Warning: The document may be modified in-place by this function!
    """

    deserializer = BsonDeserializer(
        custom_deserializers={
            t: lambda v, _: cb(v) for t, cb in custom_deserializers.items()
        },
        lazy=lazy,
    )

    return deserializer.process(document, as_type)
