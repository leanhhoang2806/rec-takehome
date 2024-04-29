from src.models.posgres_model import RestaurantAvailableTable
from src.models.pydantic_model import RestaurantAvailabilityCreate
from src.DAOs.database_session import session
from src.DAOs.base_DAO import BaseDAO


class RestaurantAvailableTableDAO(BaseDAO):
    def __init__(self) -> None:
        self.model = RestaurantAvailableTable

    def create(
        self, restaurant_availability_create: RestaurantAvailabilityCreate
    ) -> RestaurantAvailableTable:
        try:
            data_dict = self._convert_uuids_to_strings(
                restaurant_availability_create.dict()
            )
            instance = self.model(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()
