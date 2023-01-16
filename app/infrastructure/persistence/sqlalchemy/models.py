from sqlalchemy import (
    Table,
    Column,
    String,
    Boolean,
    Integer,
    UniqueConstraint,
    ForeignKeyConstraint,
    Text,
    BIGINT,
)
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import registry, composite
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION

from app.core.user.entities.user import User
from app.core.workout.entities import (
    SportsGround,
    Contact,
    Conditions,
    Location,
)
from app.core.workout.entities.liked_grounds import LikedGround


metadata = MetaData()
mapper_registry = registry(metadata=metadata)

sports_ground_table = Table(
    "sports_grounds",
    mapper_registry.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=False),
    Column("object_name", Text, nullable=False),
    Column("adm_area", Text, nullable=False),
    Column("district", Text, nullable=False),
    Column("address", Text, nullable=False),
    Column("latitude", DOUBLE_PRECISION, nullable=False),
    Column("longitude", DOUBLE_PRECISION, nullable=False),
    Column("email", Text),
    Column("phone", Text),
    Column("website", Text, nullable=False),
    Column("has_equipment_rental", Boolean, nullable=False),
    Column("has_tech_service", Boolean, nullable=False),
    Column("has_dressing_room", Boolean, nullable=False),
    Column("has_eatery", Boolean, nullable=False),
    Column("has_toilet", Boolean, nullable=False),
    Column("has_wifi", Boolean, nullable=False),
    Column("has_cash_machine", Boolean, nullable=False),
    Column("has_first_aid_post", Boolean, nullable=False),
    Column("has_music", Boolean, nullable=False),
    Column("lighting", Text, nullable=False),
    Column("seats", BIGINT, nullable=False),
    Column("paid", Text(), nullable=False),
)


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("email", String, nullable=False),
    UniqueConstraint("email", name="unique_email"),
)

liked_grounds_table = Table(
    "liked_grounds",
    mapper_registry.metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("ground_id", Integer, primary_key=True),
    ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_id",
                         ondelete="CASCADE"),
    ForeignKeyConstraint(
        ["ground_id"], ["sports_grounds.id"], name="fk_ground_id",
        ondelete="CASCADE"
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(User, user_table)
    mapper_registry.map_imperatively(LikedGround, liked_grounds_table)
    mapper_registry.map_imperatively(
        SportsGround,
        sports_ground_table,
        properties={
            "location": composite(
                Location,
                sports_ground_table.c.adm_area,
                sports_ground_table.c.district,
                sports_ground_table.c.address,
                sports_ground_table.c.latitude,
                sports_ground_table.c.longitude,
            ),
            "contact": composite(
                Contact,
                sports_ground_table.c.email,
                sports_ground_table.c.phone,
                sports_ground_table.c.website,
            ),
            "conditions": composite(
                Conditions,
                sports_ground_table.c.has_equipment_rental,
                sports_ground_table.c.has_tech_service,
                sports_ground_table.c.has_dressing_room,
                sports_ground_table.c.has_eatery,
                sports_ground_table.c.has_toilet,
                sports_ground_table.c.has_wifi,
                sports_ground_table.c.has_cash_machine,
                sports_ground_table.c.has_first_aid_post,
                sports_ground_table.c.has_music,
                sports_ground_table.c.lighting,
                sports_ground_table.c.seats,
                sports_ground_table.c.paid,
            ),
        },
    )
