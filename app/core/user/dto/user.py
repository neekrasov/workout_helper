from dataclasses import dataclass


@dataclass
class UserCreateDto:
    email: str
    username: str
    password: str
