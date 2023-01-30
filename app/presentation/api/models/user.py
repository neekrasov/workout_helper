from dataclasses import dataclass


@dataclass
class BaseUser:
    email: str
    username: str


@dataclass
class UserCreateRequest(BaseUser):
    password: str


@dataclass
class UserResponse(BaseUser):
    id: str
    hashed_password: str
