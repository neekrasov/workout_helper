from dataclasses import dataclass

from app.core.common.mediator import Command
from app.core.common.base.result import TaskId


@dataclass
class GetUpdatesCommand(Command):
    task_id: TaskId
