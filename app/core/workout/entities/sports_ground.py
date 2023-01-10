from typing import Optional
from dataclasses import dataclass, field

from app.core.common.base.entity import Entity


@dataclass
class Conditions:
    has_equipment_rental: bool
    has_tech_service: bool
    has_dressing_room: bool
    has_eatery: bool
    has_toilet: bool
    has_wifi: bool
    has_cash_machine: bool
    has_first_aid_post: bool
    has_music: bool
    lighting: str
    seats: int
    paid: bool


@dataclass
class Location:
    adm_area: str
    district: str
    address: str
    lantitude: float
    longitude: float


@dataclass
class Contact:
    email: str
    phone: str
    website: str


@dataclass
class SportsGround(Entity):
    id: Optional[int] = field()
    object_name: str
    location: Location
    contact: Contact
    conditions: Conditions
