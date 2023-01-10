import uuid
from typing import NewType, Optional
from dataclasses import dataclass, field

from app.core.common.base.entity import Entity

UserId = NewType("UserId", uuid.UUID)


@dataclass
class User(Entity):
    id: Optional[UserId] = field(init=False, default=None)
    username: str
    email: str
    hashed_password: str

    @classmethod
    def generate_id(cls) -> UserId:
        return UserId(uuid.uuid4())
