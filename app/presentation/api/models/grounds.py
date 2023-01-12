from typing import Optional
from dataclasses import dataclass


@dataclass
class CoordinatesGroundRequest:
    latitude: float
    longitude: float


@dataclass
class SearchGroundsRequest:
    object_name: Optional[str] = None
    adm_area: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    lantitude: Optional[float] = None
    longitude: Optional[float] = None
    has_equipment_rental: Optional[bool] = None
    has_tech_service: Optional[bool] = None
    has_dressing_room: Optional[bool] = None
    has_eatery: Optional[bool] = None
    has_toilet: Optional[bool] = None
    has_wifi: Optional[bool] = None
    has_cash_machine: Optional[bool] = None
    has_first_aid_post: Optional[bool] = None
    has_music: Optional[bool] = None
    lighting: Optional[str] = None
    seats: Optional[int] = None
    paid: Optional[bool] = None
