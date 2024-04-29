from src.managers.restaurant_managers import RestaurantManager
from src.managers.restaurant_availability_manager import RestaurantAvailabilityManager
from src.managers.endorsement_manager import EndorsementManager
from src.managers.eater_manager import EaterManager
from src.models.pydantic_model import (
    RestaurantCreate,
    RestaurantAvailabilityCreate,
    EndorsementCreate,
    EaterCreate,
)
from src.models.posgres_model import t_Restaurant_Endorsements, t_Dietary_Restrictions
from src.DAOs.database_session import session
import logging


def populate_data():
    restaurant_manager = RestaurantManager()
    restaurant_availability_manager = RestaurantAvailabilityManager()
    endorsement_manager = EndorsementManager()
    eater_manager = EaterManager()

    restaurant_data = {
        "Lardo": {
            "2_people_table": 4,
            "4_people_table": 2,
            "6_people_table": 1,
            "Additional_Info": "Gluten-Free",
        },
        "Panadería Rosetta": {
            "2_people_table": 3,
            "4_people_table": 2,
            "6_people_table": 0,
            "Additional_Info": "Vegetarian, Gluten-Free",
        },
        "Tetetlán": {
            "2_people_table": 4,
            "4_people_table": 2,
            "6_people_table": 1,
            "Additional_Info": "paleo, Gluten-Free",
        },
        "Falling Piano Brewing Co": {
            "2_people_table": 5,
            "4_people_table": 5,
            "6_people_table": 5,
            "Additional_Info": "",
        },
        "u.to.pi.a": {
            "2_people_table": 2,
            "4_people_table": 0,
            "6_people_table": 0,
            "Additional_Info": "Vegan, Vegetarian",
        },
    }

    eater_data = [
        {
            "Name": "Michael",
            "Home Location": "19.4153107,-99.1804722",
            "Dietary Restrictions": "Vegetarian",
        },
        {
            "Name": "George Michael",
            "Home Location": "19.4058242,-99.1671942",
            "Dietary Restrictions": "Vegetarian, Gluten-Free",
        },
        {
            "Name": "Lucile",
            "Home Location": "19.3634215,-99.1769323",
            "Dietary Restrictions": "Gluten-Free",
        },
        {
            "Name": "Gob",
            "Home Location": "19.3318331,-99.2078983",
            "Dietary Restrictions": "Paleo",
        },
        {
            "Name": "Tobias",
            "Home Location": "19.4384214,-99.2036906",
            "Dietary Restrictions": "",
        },
        {
            "Name": "Maeby",
            "Home Location": "19.4349474,-99.1419256",
            "Dietary Restrictions": "Vegan",
        },
    ]

    names = restaurant_data.keys()

    seen_endorsement = {}
    for name in names:
        restaurant = restaurant_manager.create(RestaurantCreate(name=name))
        restaurant_availability = RestaurantAvailabilityCreate(
            restaurant_id=restaurant.id,
            two_people_table=restaurant_data[name]["2_people_table"],
            four_people_table=restaurant_data[name]["4_people_table"],
            six_people_table=restaurant_data[name]["6_people_table"],
        )
        restaurant_availability_manager.create(restaurant_availability)
        restaurant_endorsements = [
            part.strip().lower()
            for part in restaurant_data[name]["Additional_Info"].split(",")
        ]

        for endor in restaurant_endorsements:
            if not endor:
                continue
            if endor not in seen_endorsement:
                inserted_endorsement = endorsement_manager.create(
                    EndorsementCreate(endorsement=endor)
                )
                seen_endorsement[endor] = inserted_endorsement.id
            session.execute(
                t_Restaurant_Endorsements.insert(),
                {
                    "restaurant_id": str(restaurant.id),
                    "endorsement_id": str(seen_endorsement[endor]),
                },
            )

    for eater in eater_data:
        eater_instance = eater_manager.create(EaterCreate(name=eater["Name"]))
        if not eater["Dietary Restrictions"]:
            continue
        diet = [
            part.strip().lower() for part in eater["Dietary Restrictions"].split(",")
        ]

        for i in diet:
            session.execute(
                t_Dietary_Restrictions.insert(),
                {"eater_id": str(eater_instance.id), "diet_name": i},
            )
    session.commit()

    logging.info("Finished populating restaurant names")
