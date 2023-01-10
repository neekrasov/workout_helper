from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.user.protocols.token_gateway import SessionId


@dataclass
class GetCurrentUserCommand(Command):
    session_id: SessionId
