from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.types import SessionId


@dataclass
class GetCurrentUserCommand(Command):
    session_id: SessionId
