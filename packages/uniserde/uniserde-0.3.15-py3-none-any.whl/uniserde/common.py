from __future__ import annotations

import dataclasses
import inspect
import types
import typing as t

import typing_extensions as te

__all__ = [
    "SerdeError",
    "as_child",
    "get_fields",
]


T = t.TypeVar("T")


Recur: te.TypeAlias = t.Callable[[t.Any, t.Type], t.Any]
Serializer: te.TypeAlias = t.Callable[[t.Any, t.Type, Recur], t.Any]
Deserializer: te.TypeAlias = t.Callable[[t.Any, t.Type, Recur], t.Any]


class SerdeError(Exception):
    """
    Signals an error during serialization or deserialization.
    """

    def __init__(self, user_message: str):
        self.user_message = user_message


def as_child(cls: t.Type[T]) -> t.Type[T]:
    """
    Marks the class to be serialized as one of its children. This will add an
    additional "type" field in the result, so the child can be deserialized
    properly.

    This decorator applies to children of the class as well, i.e. they will also
    be serialized with the "type" field.
    """
    assert inspect.isclass(cls), cls
    cls.__serde_serialize_as_child__ = cls  # type: ignore
    return cls


def should_serialize_as_child(cls: t.Type) -> bool:
    """
    Checks whether the given class should be serialized as a child, i.e. it, or
    any parent has been marked with the `as_child` decorator.
    """
    assert inspect.isclass(cls), cls
    return hasattr(cls, "__serde_serialize_as_child__")


def get_type_key(cls: t.Type) -> t.Type:
    """
    Given a type, return a more standardized type, suitable for use as a key to
    find serializers/deserializers.
    """

    # See what `get_origin` can do
    result: t.Any = t.get_origin(cls)

    if result is None:
        result = cls

    # Convert new-style unions to old-style
    if result is types.UnionType:
        result = t.Union

    # Pass through the rest
    return result


def common_serialize(
    value: t.Any,
    value_type: t.Type | None,
    class_serializer: Serializer,
    serializers: dict[t.Type, Serializer],
    user_serializers: dict[t.Type, t.Callable[[t.Any], t.Any]],
) -> t.Any:
    # Find the type
    if value_type is None:
        value_type = type(value)

    # Is there a custom serializer for this class?
    try:
        serializer = user_serializers[value_type]
    except KeyError:
        pass
    else:
        return serializer(value)

    # Find a matching serializer
    key = get_type_key(value_type)

    try:
        serializer = serializers[key]
    except KeyError:
        if inspect.isclass(value_type):
            serializer = class_serializer
        else:
            raise ValueError(f"Unsupported field of type {value_type}") from None

    # Define the recursion function
    def recur(value: t.Any, value_type: t.Type) -> t.Any:
        return common_serialize(
            value,
            value_type,
            class_serializer,
            serializers,
            user_serializers,
        )

    # Apply it
    return serializer(value, value_type, recur)


def common_deserialize(
    value: t.Any,
    value_type: t.Type,
    class_deserializer: Serializer,
    deserializers: dict[t.Type, Deserializer],
    user_deserializers: dict[t.Type, t.Callable[[t.Any], t.Any]],
) -> t.Any:
    # Is there a custom deserializer for this class?
    try:
        deserializer = user_deserializers[value_type]
    except KeyError:
        pass
    else:
        return deserializer(value)

    # Find a matching serializer
    key = get_type_key(value_type)

    try:
        deserializer = deserializers[key]
    except KeyError:
        if inspect.isclass(value_type):
            deserializer = class_deserializer
        else:
            raise ValueError(f"Unsupported field of type {value_type}") from None

    # Define the recursion function
    def recur(value: t.Any, value_type: t.Type) -> t.Any:
        return common_deserialize(
            value,
            value_type,
            class_deserializer,
            deserializers,
            user_deserializers,
        )

    # Apply it
    return deserializer(value, value_type, recur)


def all_subclasses(cls: t.Type, include_cls: bool) -> t.Iterable[t.Type]:
    """
    Yields all classes directly on indirectly inheriting from `cls`. Does not
    perform any sort of cycle checks.

    :param cls: The class to start from.
    :param include_cls: Whether to include `cls` itself in the results.
    """

    if include_cls:
        yield cls

    for subclass in cls.__subclasses__():
        yield from all_subclasses(subclass, include_cls=True)


def custom_get_type_hints(typ: t.Type) -> dict[str, t.Type]:
    """
    Returns the type hints for the given type, applying some uniserde specific
    logic.
    """
    hints = t.get_type_hints(typ)

    # Drop any value named '_' if it's just `dataclasses.KW_ONLY`
    if hasattr(typ, "__dataclass_fields__"):
        try:
            val = hints["_"]
        except KeyError:
            pass
        else:
            if val is dataclasses.KW_ONLY:
                del hints["_"]

    return hints


def get_fields(cls: t.Type) -> dict[str, t.Type]:
    """
    Returns the names and types of all fields in the class. Fields are
    determined from type hints, with some custom logic applied:

    - For dataclasses, fields named `_` are dropped if their type hint is
      `dataclasses.KW_ONLY`.

    The types are standardized according to some rules:

    - New-style unions are converted to old-style (`types.UnionType` ->
      `typing.Union`).
    """

    result: dict[str, t.Type] = {}

    # Get all fields. This will already drop `KW_ONLY` fields.
    for name, typ in custom_get_type_hints(cls).items():
        # Convert new-style unions to old-style
        if isinstance(typ, types.UnionType):
            typ = Union[*get_args(typ)]  # type: ignore

        # Store the result
        result[name] = typ

    return result
