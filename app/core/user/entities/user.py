from dataclasses import dataclass

from app.core.common.entity import Entity


@dataclass
class User(Entity):
    username: str
    email: str
    hashed_password: str
