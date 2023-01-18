import uuid
import re
from typing import Optional
from dataclasses import dataclass, field

from app.core.common.base.entity import Entity
from app.core.common.base.types import UserId
from app.core.common.base.exceptions import ValidationError


@dataclass
class Username(str):
    value: str

    def __post_init__(self):
        v = self.value

        if not isinstance(v, str):
            raise ValidationError("Username must be a string")

        if len(v) < 3:
            raise ValidationError(
                "Username must be at least 3 characters long"
            )

        if len(v) > 32:
            raise ValidationError(
                "Username must be at most 32 characters long"
            )

        if " " in v:
            raise ValidationError("Username must not contain spaces")

        if v[0].isnumeric():
            raise ValidationError("Username must not start with a digit")

        regex = r"[!@#$%^&*\-()_+]+"
        if re.search(regex, v):
            raise ValidationError(
                "Username must not contain special characters"
            )

        if v.isnumeric():
            raise ValidationError("Username must not be numeric")


@dataclass
class Email(str):
    value: str

    def __post_init__(self):
        v = self.value

        if not isinstance(v, str):
            raise ValidationError("Email must be a string")

        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.search(regex, v):
            raise ValidationError("Email is invalid")


@dataclass
class RawPassword(str):
    value: str

    def __post_init__(self):
        v = self.value

        if not isinstance(v, str):
            raise ValidationError("Password must be a string")

        if len(v) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long"
            )

        if len(v) > 64:
            raise ValidationError(
                "Password must be at most 64 characters long"
            )

        regex = r"[a-z]+"
        if not re.search(regex, v):
            raise ValidationError("Password must contain a lowercase letter")

        regex = r"[A-Z]+"
        if not re.search(regex, v):
            raise ValidationError("Password must contain an uppercase letter")

        regex = r"[0-9]+"
        if not re.search(regex, v):
            raise ValidationError("Password must contain a number")

        regex = r"[!@#$%^&*\-()_+]+"
        if not re.search(regex, v):
            raise ValidationError("Password must contain a special character")


@dataclass
class User(Entity):
    id: Optional[UserId] = field(init=False, default=None)
    username: Username
    email: Email
    hashed_password: str

    @classmethod
    def generate_id(cls) -> UserId:
        return UserId(uuid.uuid4())
