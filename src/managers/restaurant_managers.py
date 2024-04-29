from src.DAOs.restaurant_DAO import RestaurantDAO
from src.models.pydantic_model import RestaurantCreate
from src.models.posgres_model import Restaurant
from uuid import UUID
from typing import List, Optional
import datetime


class RestaurantManager:
    def __init__(self) -> None:
        self.dao = RestaurantDAO()

    def create(self, restaurant_create: RestaurantCreate) -> Restaurant:
        return self.dao.create(restaurant_create)

    def reservation_search(self, eaters: List[UUID]) -> Optional[Restaurant]:
        return self.dao.reservation_search(eaters)
