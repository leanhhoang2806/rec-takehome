from src.routes.custom_route import CustomAPIRouter
from src.managers.eater_manager import EaterManager
from src.managers.restaurant_managers import RestaurantManager
from src.managers.reservation_manager import ReservationManager
from src.models.posgres_model import RestaurantPydantic, ReservationPydantic
from src.models.pydantic_model import ReservationCreate
from typing import List, Optional
from datetime import datetime
from fastapi import Query
from uuid import UUID
import logging


router = CustomAPIRouter()
eater_manager = EaterManager()
restaurant_manager = RestaurantManager()
reservation_manager = ReservationManager()


@router.get("/search/restaurants", response_model=Optional[List[RestaurantPydantic]])
async def get_available_table(
    eaters: List[UUID] = Query(...),
):
    restaurants = restaurant_manager.reservation_search(eaters)
    return (
        [RestaurantPydantic.from_orm(restaurant) for restaurant in restaurants]
        if restaurants
        else None
    )


@router.post("/reservation", response_model=ReservationPydantic)
async def create_reservation(reservation_create: ReservationCreate):
    eater_info = [
        eater_manager.get_eater_by_name(eater) for eater in reservation_create.eaters
    ]
    eaters = [eater.id for eater in eater_info]
    reservation = reservation_manager.create(eaters, reservation_create)
    return ReservationPydantic.from_orm(reservation)


@router.delete("/reservation/{reservation_id}")
async def delete_reservation(reservation_id: UUID):
    return reservation_manager.delete(reservation_id)


@router.get("/user/{name}")
async def get_all_user(name: str):
    return eater_manager.get_eater_by_name(name)
