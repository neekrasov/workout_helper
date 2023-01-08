from dataclasses import dataclass
from app.core.common.cqs import Query


@dataclass
class GetUserByEmailQuery(Query):
    email: str
