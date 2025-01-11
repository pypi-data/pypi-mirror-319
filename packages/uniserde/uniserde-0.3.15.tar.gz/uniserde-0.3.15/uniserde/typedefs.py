from __future__ import annotations

import typing as t
from datetime import datetime

import typing_extensions as te

from .objectid_proxy import ObjectId

__all__ = [
    "Jsonable",
    "Bsonable",
    "JsonDoc",
    "BsonDoc",
]


Jsonable: te.TypeAlias = t.Union[
    None,
    bool,
    int,
    float,
    str,
    dict[str, "Jsonable"],
    list["Jsonable"],
    tuple["Jsonable", ...],
]

Bsonable: te.TypeAlias = t.Union[
    None,
    bool,
    int,
    float,
    str,
    dict[str, "Bsonable"],
    list["Bsonable"],
    tuple["Bsonable", ...],
    bytes,
    ObjectId,
    datetime,
]

JsonDoc = dict[str, Jsonable]
BsonDoc = dict[str, Bsonable]
