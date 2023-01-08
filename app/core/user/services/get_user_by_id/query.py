from uuid import UUID
from dataclasses import dataclass
from app.core.common.cqs import Query


@dataclass
class GetUserByIDQuery(Query):
    user_id: UUID
