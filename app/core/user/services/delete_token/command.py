from uuid import UUID
from dataclasses import dataclass
from app.core.common.cqs import Command


@dataclass
class DeleteTokenCommand(Command):
    session_id: UUID
