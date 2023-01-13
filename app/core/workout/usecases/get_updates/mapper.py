from typing import List

from app.core.common.base.types import GroundId
from app.core.workout.entities import (
    SportsGround,
    Conditions,
    Contact,
    Location,
)


class CalculationsToListEntityMapper:
    @staticmethod
    def map(data: dict) -> List[SportsGround]:
        grounds_list = []

        for item in data.items():
            grounds_list.append(
                SportsGround(
                    id=GroundId(int(item[1]["id"])),
                    object_name=item[1]["object_name"],
                    location=Location(
                        adm_area=item[1]["adm_area"],
                        district=item[1]["district"],
                        address=item[1]["address"],
                        latitude=item[1]["latitude"],
                        longitude=item[1]["longitude"],
                    ),
                    contact=Contact(
                        email=item[1]["email"],
                        website=item[1]["website"],
                        phone=item[1]["phone"]
                    ),
                    conditions=Conditions(
                        has_equipment_rental=item[1]["has_equipment_rental"],
                        has_tech_service=item[1]["has_tech_service"],
                        has_dressing_room=item[1]["has_dressing_room"],
                        has_eatery=item[1]["has_eatery"],
                        has_toilet=item[1]["has_toilet"],
                        has_wifi=item[1]["has_wifi"],
                        has_cash_machine=item[1]["has_cash_machine"],
                        has_first_aid_post=item[1]["has_first_aid_post"],
                        has_music=item[1]["has_music"],
                        lighting=item[1]["lighting"],
                        seats=item[1]["seats"],
                        paid=item[1]["paid"]
                    )
                )
            )
        return grounds_list
