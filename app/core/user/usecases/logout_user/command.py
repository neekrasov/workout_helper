from dataclasses import dataclass

from app.core.common.mediator import Command
from ...protocols.token_gateway import SessionId


@dataclass
class LogoutUserCommand(Command):
    session_id: SessionId
