from typing import List

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
                    id=int(item[1]["global_id"]),
                    object_name=item[1]["ObjectName"],
                    location=Location(
                        adm_area=item[1]["AdmArea"],
                        district=item[1]["District"],
                        address=item[1]["Address"],
                        lantitude=item[1]["latitude"],
                        longitude=item[1]["longitude"],
                    ),
                    contact=Contact(
                        email=item[1]["Email"],
                        website=item[1]["WebSite"],
                        phone=item[1]["HelpPhone"]
                    ),
                    conditions=Conditions(
                        has_equipment_rental=item[1]["HasEquipmentRental"],
                        has_tech_service=item[1]["HasTechService"],
                        has_dressing_room=item[1]["HasDressingRoom"],
                        has_eatery=item[1]["HasEatery"],
                        has_toilet=item[1]["HasToilet"],
                        has_wifi=item[1]["HasWifi"],
                        has_cash_machine=item[1]["HasCashMachine"],
                        has_first_aid_post=item[1]["HasFirstAidPost"],
                        has_music=item[1]["HasMusic"],
                        lighting=item[1]["Lighting"],
                        seats=item[1]["Seats"],
                        paid=item[1]["Paid"]
                    )
                )
            )
        return grounds_list
