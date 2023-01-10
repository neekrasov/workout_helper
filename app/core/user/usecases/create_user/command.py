from dataclasses import dataclass

from app.core.common.mediator import Command


@dataclass
class CreateUserCommand(Command):
    username: str
    email: str
    password: str
