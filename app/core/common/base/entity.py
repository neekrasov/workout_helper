from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Entity:
    id: UUID = field(init=False)

    @classmethod
    def generate_id(cls) -> UUID:
        return uuid4()
