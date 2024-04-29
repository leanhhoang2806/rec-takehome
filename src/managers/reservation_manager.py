from src.DAOs.reservation_DAO import ReservationDAO
from src.models.posgres_model import Reservation
from src.models.pydantic_model import ReservationCreate
from typing import Optional, List
from uuid import UUID
from src.errors.custom_errors import ExistingReservationDuringTimeFrame
import datetime


class ReservationManager:
    def __init__(self) -> None:
        self.dao = ReservationDAO()

    def create(
        self, eater_ids: List[UUID], reservation_create: ReservationCreate
    ) -> Reservation:
        return self.dao.create(eater_ids, reservation_create)

    def delete(self, reservation_id: UUID) -> int:
        return self.dao.delete(reservation_id)
