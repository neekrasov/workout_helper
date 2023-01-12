from typing import Optional
from dataclasses import dataclass, field

from app.core.common.base.entity import Entity
from app.core.common.base.types import GroundId


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
    paid: str

    def __composite_values__(self):
        return (
            self.has_equipment_rental,
            self.has_tech_service,
            self.has_dressing_room,
            self.has_eatery,
            self.has_toilet,
            self.has_wifi,
            self.has_cash_machine,
            self.has_first_aid_post,
            self.has_music,
            self.lighting,
            self.seats,
            self.paid,
        )


@dataclass
class Location:
    adm_area: str
    district: str
    address: str
    latitude: float
    longitude: float

    def __composite_values__(self):
        return (
            self.adm_area,
            self.district,
            self.address,
            self.latitude,
            self.longitude,
        )


@dataclass
class Contact:
    email: str
    phone: str
    website: str

    def __composite_values__(self):
        return (
            self.email,
            self.phone,
            self.website,
        )


@dataclass
class SportsGround(Entity):
    id: Optional[GroundId] = field()
    object_name: str
    location: Location
    contact: Contact
    conditions: Conditions
