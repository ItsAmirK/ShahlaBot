from dataclasses import dataclass, field, asdict
from typing import Any, TypeVar

from bson.objectid import ObjectId


_T = TypeVar("_T", bound="ModelBase")


def deserialize(cls: type[_T], data: dict[str, Any] | None) -> _T | None:
    if data is None:
        return None
    return cls(**data)


@dataclass()
class ModelBase:
    _id: ObjectId | None = field(default=None, kw_only=True)

    def serialize(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def deserialize(cls: type[_T], data: dict[str, Any] | None) -> _T | None:
        return deserialize(cls, data)
