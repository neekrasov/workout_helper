from sqlalchemy import Table, Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from app.core.user.entities.user import User
from . import mapper_registry


user_table = Table(
    "users", mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("email", String, nullable=False),
    UniqueConstraint("email", name="unique_email"),
)


def map_user_table(mapper_registry: registry):
    mapper_registry.map_imperatively(User, user_table)
