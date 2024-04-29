from src.models.posgres_model import Endorsement
from src.DAOs.base_DAO import BaseDAO
from src.models.pydantic_model import EndorsementCreate
from src.DAOs.database_session import session


class EndorsementDAO(BaseDAO):
    def __init__(self) -> None:
        self.model = Endorsement

    def create(self, endorsement_create: EndorsementCreate) -> Endorsement:
        try:
            instance = self.model(**endorsement_create.dict())
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()
