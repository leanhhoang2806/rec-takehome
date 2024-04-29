from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class RestaurantCreate(BaseModel):
    name: str


class Configuration(BaseModel):
    POSTGRES_DATABASE_URL_CONNECTION_STRING: str


class RestaurantAvailabilityCreate(BaseModel):
    restaurant_id: UUID
    two_people_table: int
    four_people_table: int
    six_people_table: int


class EndorsementCreate(BaseModel):
    endorsement: str


class EaterCreate(BaseModel):
    name: str


class EaterDiet(BaseModel):
    diet_name: str


class ReservationCreate(BaseModel):
    restaurant_id: UUID
    created_at: datetime
    eaters: List[str]
