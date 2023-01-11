from app.core.common.mediator import UseCase
from app.core.common.base.result import TaskId, CalculationResult
from ....protocols.analysis import AnalysisSportsGround
from .command import SearchGroundsCommand


class SearchGroundsUseCase(UseCase):
    def __init__(self, analysis: AnalysisSportsGround):
        self.analysis = analysis

    async def handle(
        self, command: SearchGroundsCommand
    ) -> CalculationResult[TaskId]:
        search_query = self._prepare_dict_to_search_string(
            command.search_params
        )
        return self.analysis.search_grounds(search_query, command.count)

    def _prepare_dict_to_search_string(self, dict: dict) -> str:
        values = []
        for k, v in dict.items():

            if v is None:
                continue

            if type(v) is bool:
                v = self._t_f_to_string(v)

            item = f"{k.title().replace('_', '')}: {v} "
            values.append(item)

        return " ".join(values)

    def _t_f_to_string(self, value: bool) -> str:
        return "да" if value else "нет"
