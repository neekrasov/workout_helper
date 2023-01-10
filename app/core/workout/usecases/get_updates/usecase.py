from app.core.common.mediator import UseCase

from ...protocols.analysis import AnalysisSportsGround, UpdatesResult
from .command import GetUpdatesCommand
from .mapper import CalculationsToListEntityMapper


class GetUpdatesHandler(UseCase[GetUpdatesCommand, UpdatesResult]):
    def __init__(self, analysis: AnalysisSportsGround) -> None:
        self._analysis = analysis
        self._mapper = CalculationsToListEntityMapper()

    async def handle(self, command: GetUpdatesCommand) -> UpdatesResult:
        updates = self._analysis.get_updates(command.task_id)
        if type(updates.data) is dict:
            updates.data = self._mapper.map(updates.data)
        return updates
