from src.DAOs.restaurant_available_table_DAO import RestaurantAvailableTableDAO
from src.models.pydantic_model import RestaurantAvailabilityCreate
from src.models.posgres_model import RestaurantAvailableTable


class RestaurantAvailabilityManager:
    def __init__(self) -> None:
        self.dao = RestaurantAvailableTableDAO()

    def create(
        self, restaurant_availability_create: RestaurantAvailabilityCreate
    ) -> RestaurantAvailableTable:
        return self.dao.create(restaurant_availability_create)
