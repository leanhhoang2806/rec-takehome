from src.models.posgres_model import Reservation, t_Reservation_Eater
from src.DAOs.database_session import session
from src.models.pydantic_model import ReservationCreate
from uuid import UUID
from datetime import timedelta
from sqlalchemy import and_
from typing import List

from src.models.posgres_model import RestaurantAvailableTable, Reservation, Restaurant
from src.DAOs.database_session import session
from sqlalchemy import func, and_, insert, update
from sqlalchemy.sql.expression import Selectable
from src.errors.custom_errors import (
    ExistingReservationDuringTimeFrame,
    RestaurantCantFulfillReservation,
)


class ReservationDAO:
    def __init__(self) -> None:
        self.model = Reservation

    def create(
        self, eater_ids: List[UUID], reservation_create: ReservationCreate
    ) -> Reservation:
        num_eaters = len(eater_ids)
        seat_columns = {
            1: "two_people_table",
            2: "two_people_table",
            3: "four_people_table",
            4: "four_people_table",
            5: "six_people_table",
            6: "six_people_table",
        }
        seat_column = seat_columns.get(num_eaters, "six_people_table")
        seat_availability_filters = None
        if num_eaters < 2:
            seat_availability_filters = RestaurantAvailableTable.two_people_table > 0
        elif num_eaters < 4 and num_eaters > 2:
            seat_availability_filters = RestaurantAvailableTable.four_people_table > 0
        elif num_eaters < 6 and num_eaters > 4:
            seat_availability_filters = RestaurantAvailableTable.six_people_table > 0
        else:
            seat_availability_filters = func.array_length(eater_ids, 1) >= 6
        try:
            two_hours_before = reservation_create.created_at - timedelta(hours=2)
            two_hours_after = reservation_create.created_at + timedelta(hours=2)
            five_minutes_before = reservation_create.created_at - timedelta(minutes=5)
            five_minutes_after = reservation_create.created_at + timedelta(minutes=5)

            session.begin()

            is_there_reservation: Selectable = (
                session.query(Reservation)
                .join(t_Reservation_Eater)
                .filter(
                    and_(
                        t_Reservation_Eater.c.eater_id.in_(
                            [str(eater_id) for eater_id in eater_ids]
                        ),
                        Reservation.created_at.between(
                            two_hours_before, two_hours_after
                        ),
                    )
                )
                .all()
            )

            if is_there_reservation:
                raise ExistingReservationDuringTimeFrame

            available_tables_query = (
                session.query(Restaurant)
                .join(RestaurantAvailableTable)
                .outerjoin(
                    Reservation,
                    and_(
                        Reservation.created_at.between(
                            five_minutes_before, five_minutes_after
                        )
                    ),
                )
                .filter(
                    seat_availability_filters,
                    Restaurant.id == str(reservation_create.restaurant_id),
                )
                .all()
            )

            if not available_tables_query:
                raise RestaurantCantFulfillReservation

            # All checks pass, post the reservation
            reservation_data = {
                "created_at": reservation_create.created_at,
                "restaurant_id": str(reservation_create.restaurant_id),
            }
            instance = Reservation(**reservation_data)
            session.add(instance)

            session.commit()
            for eater_id in eater_ids:
                session.execute(
                    insert(t_Reservation_Eater).values(
                        reservation_id=instance.id, eater_id=str(eater_id)
                    )
                )

            if seat_column == "two_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation_create.restaurant_id)
                    )
                    .values(
                        two_people_table=RestaurantAvailableTable.two_people_table - 1
                    )
                )
            elif seat_column == "four_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation_create.restaurant_id)
                    )
                    .values(
                        four_people_table=RestaurantAvailableTable.four_people_table - 1
                    )
                )
            elif seat_column == "six_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation_create.restaurant_id)
                    )
                    .values(
                        six_people_table=RestaurantAvailableTable.six_people_table - 1
                    )
                )

            session.execute(stmt)
            session.commit()
            session.refresh(instance)
            return instance
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, reservation_id: UUID) -> int:
        try:
            reservation: Reservation = (
                session.query(Reservation)
                .filter(Reservation.id == str(reservation_id))
                .first()
            )
            eaters = (
                session.query(Reservation)
                .join(t_Reservation_Eater)
                .filter(Reservation.id == str(reservation_id))
                .all()
            )
            seat_columns = {
                1: "two_people_table",
                2: "two_people_table",
                3: "four_people_table",
                4: "four_people_table",
                5: "six_people_table",
                6: "six_people_table",
            }
            seat_column = seat_columns.get(len(eaters), "six_people_table")
            session.query(t_Reservation_Eater).filter(
                t_Reservation_Eater.c.reservation_id == str(reservation_id)
            ).delete()

            session.query(Reservation).filter(
                Reservation.id == str(reservation_id)
            ).delete()

            if seat_column == "two_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation.restaurant_id)
                    )
                    .values(
                        two_people_table=RestaurantAvailableTable.two_people_table + 1
                    )
                )
            elif seat_column == "four_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation.restaurant_id)
                    )
                    .values(
                        four_people_table=RestaurantAvailableTable.four_people_table + 1
                    )
                )
            elif seat_column == "six_people_table":
                stmt = (
                    update(RestaurantAvailableTable)
                    .where(
                        RestaurantAvailableTable.restaurant_id
                        == str(reservation.restaurant_id)
                    )
                    .values(
                        six_people_table=RestaurantAvailableTable.six_people_table + 1
                    )
                )
            session.execute(stmt)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
