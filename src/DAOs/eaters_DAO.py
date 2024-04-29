from src.models.posgres_model import Eater
from src.models.pydantic_model import EaterCreate
from src.DAOs.base_DAO import BaseDAO
from src.DAOs.database_session import session
from typing import Optional


class EaterDAO(BaseDAO):
    def __init__(self) -> None:
        self.model = Eater

    def create(self, eater: EaterCreate) -> Eater:
        try:
            data_dict = self._convert_uuids_to_strings(eater.dict())
            instance = Eater(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get_eater_by_name(self, name: str) -> Optional[Eater]:
        try:
            return session.query(Eater).filter(Eater.name == name).first()
        finally:
            session.close()
