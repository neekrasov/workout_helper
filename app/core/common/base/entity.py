from typing import Optional, TypeVar, Generic
from dataclasses import dataclass, field

ID = TypeVar("ID")


@dataclass
class Entity(Generic[ID]):
    id: Optional[ID] = field(init=False, default=None)

    @classmethod
    def generate_id(cls) -> ID:
        raise NotImplementedError
