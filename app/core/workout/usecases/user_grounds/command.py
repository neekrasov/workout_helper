from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.types import UserId


@dataclass
class GetUserGroundsCommand(Command):
    user_id: UserId
