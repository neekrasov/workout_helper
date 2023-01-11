from dataclasses import dataclass

from app.core.common.mediator import Command


@dataclass
class CalculateSearchGroundsCommand(Command):
    search_query: str
    count: int
