from dataclasses import dataclass


@dataclass
class UserCreateRequest:
    email: str
    username: str
    password: str
