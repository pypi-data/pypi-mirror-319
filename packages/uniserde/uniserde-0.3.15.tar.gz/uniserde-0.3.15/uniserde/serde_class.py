from __future__ import annotations

import typing as t

import uniserde

from .typedefs import *

__all__ = [
    "Serde",
]


T = t.TypeVar("T", bound="Serde")


class Serde:
    def as_bson(
        self,
        *,
        as_type: t.Optional[t.Type] = None,
        custom_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> BsonDoc:
        """
        Serialize the entire instance to BSON, by applying the field serializer
        to each field. Field names are converted to camel case.
        """
        assert as_type is None or issubclass(self.__class__, as_type), as_type
        return uniserde.as_bson(
            self,
            as_type=as_type,
            custom_serializers=custom_serializers,
        )  # type: ignore

    def as_json(
        self,
        *,
        as_type: t.Optional[t.Type] = None,
        custom_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> JsonDoc:
        """
        Serialize the entire instance to JSON, by applying the field serializer
        to each field. Field names are converted to camel case.
        """
        assert as_type is None or issubclass(self.__class__, as_type), as_type
        return uniserde.as_json(
            self,
            as_type=as_type,
            custom_serializers=custom_serializers,
        )  # type: ignore

    @classmethod
    def from_bson(
        cls: t.Type[T],
        document: BsonDoc,
        *,
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
        lazy: bool = False,
    ) -> T:
        """
        Deserialize an entire data class from BSON, by applying the field
        deserializer to each field. Field names are converted from camel case.

        Warning: The document may be modified in-place by this function!
        """
        return uniserde.from_bson(
            document,
            as_type=cls,
            custom_deserializers=custom_deserializers,
            lazy=lazy,
        )

    @classmethod
    def from_json(
        cls: t.Type[T],
        document: JsonDoc,
        *,
        custom_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
        lazy: bool = False,
    ) -> T:
        """
        Deserialize an entire class from JSON, by applying the field
        deserializer to each field. Field names are converted from camel case.

        Warning: The document may be modified in-place by this function!
        """
        return uniserde.from_json(
            document,
            as_type=cls,
            custom_deserializers=custom_deserializers,
            lazy=lazy,
        )

    @classmethod
    def as_mongodb_schema(
        cls,
        *,
        custom_handlers: dict[t.Type, t.Callable[[t.Any], t.Any]] = {},
    ) -> t.Any:
        """
        Return a MongoDB schema for this class. The schema matches values
        resulting from `as_bson`.
        """
        return uniserde.as_mongodb_schema(
            cls,
            custom_handlers=custom_handlers,
        )
