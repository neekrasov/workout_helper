from uuid import UUID
from dataclasses import dataclass
from app.core.common.cqs import Query


@dataclass
class GetTokenQuery(Query):
    session_id: UUID
