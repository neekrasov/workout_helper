from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from app.core.user.entities.user import User


metadata = MetaData()

user = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
)


def start_mappers():
    mapper_registry = registry()

    mapper_registry.map_imperatively(User, user)
