from dataclasses import dataclass
from app.core.common.mediator import Command


@dataclass
class LoginUserCommand(Command):
    email: str
    raw_password: str
