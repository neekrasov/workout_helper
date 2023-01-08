from uuid import UUID
from dataclasses import dataclass
from app.core.common.cqs import Command


@dataclass
class CreateTokenCommand(Command):
    user_id: UUID
    session_id: UUID
