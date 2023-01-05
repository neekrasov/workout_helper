from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass
class Entity:
    id: UUID

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def generate_id(cls) -> UUID:
        return uuid4()
