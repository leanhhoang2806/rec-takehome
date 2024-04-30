from src.models.posgres_model import (
    Restaurant,
    t_Dietary_Restrictions,
    t_Restaurant_Endorsements,
    Endorsement,
    RestaurantAvailableTable,
    Reservation
)
from src.models.pydantic_model import RestaurantCreate
from src.DAOs.database_session import session
from src.DAOs.base_DAO import BaseDAO
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func, and_


class RestaurantDAO(BaseDAO):
    def __init__(self) -> None:
        self.model = Restaurant

    def create(self, restaurant_create: RestaurantCreate) -> Restaurant:
        try:
            data_dict = self._convert_uuids_to_strings(restaurant_create.dict())
            instance = self.model(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def reservation_search(self, eater_ids: List[UUID], time: datetime) -> Optional[Restaurant]:
        five_minutes_before = time - timedelta(minutes=5)
        five_minutes_after = time + timedelta(minutes=5)
        try:

            eater_diet_query = (
                session.query(t_Dietary_Restrictions)
                .filter(
                    t_Dietary_Restrictions.c.eater_id.in_(
                        [str(eater_id) for eater_id in eater_ids]
                    )
                )
                .all()
            )

            # Extract the distinct diet names from the dietary restrictions
            diet_names = set([diet.diet_name for diet in eater_diet_query])

            endorsement_query = (
                session.query(Endorsement)
                .filter(Endorsement.endorsement.in_(diet_names))
                .all()
            )
            endorsement_diet_names = set(
                [endorsement.endorsement for endorsement in endorsement_query]
            )
            if len(endorsement_diet_names) != len(diet_names):
                return None

            # Extract the endorsement IDs from the filtered endorsements
            endorsement_ids = [endorsement.id for endorsement in endorsement_query]

            subquery = (
                session.query(
                    t_Restaurant_Endorsements.c.restaurant_id,
                    func.count(t_Restaurant_Endorsements.c.endorsement_id).label(
                        "count"
                    ),
                )
                .filter(t_Restaurant_Endorsements.c.endorsement_id.in_(endorsement_ids))
                .group_by(t_Restaurant_Endorsements.c.restaurant_id)
                .subquery()
            )

            # Query the Restaurant table and join with the subquery to filter by the count of endorsement IDs
            available_tables_query = (
                session.query(Restaurant)
                .join(subquery, subquery.c.restaurant_id == Restaurant.id)
                .join(RestaurantAvailableTable)
                .outerjoin(
                    Reservation,
                    and_(
                        Reservation.created_at.between(
                            five_minutes_before, five_minutes_after
                        )
                    ),
                )
                .filter(subquery.c.count == len(endorsement_ids))
                .all()
            )

            return available_tables_query
        finally:
            session.close()
