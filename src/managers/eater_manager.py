from src.DAOs.eaters_DAO import EaterDAO
from src.models.pydantic_model import EaterCreate
from src.models.posgres_model import Eater
from typing import Optional
from src.errors.custom_errors import EaterNotExist
import logging


class EaterManager:
    def __init__(self) -> None:
        self.dao = EaterDAO()

    def create(self, eater_create: EaterCreate) -> Eater:
        return self.dao.create(eater_create)

    def get_eater_by_name(self, name: str) -> Optional[Eater]:
        result = self.dao.get_eater_by_name(name)
        if not result:
            raise EaterNotExist
        return result
