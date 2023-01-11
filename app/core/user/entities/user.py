import uuid
from typing import Optional
from dataclasses import dataclass, field

from app.core.common.base.entity import Entity
from app.core.common.base.types import UserId


@dataclass
class User(Entity):
    id: Optional[UserId] = field(init=False, default=None)
    username: str
    email: str
    hashed_password: str

    @classmethod
    def generate_id(cls) -> UserId:
        return UserId(uuid.uuid4())
