from dataclasses import dataclass

from app.core.common.mediator import Command


@dataclass
class SearchGroundsCommand(Command):
    search_params: dict
    count: int
