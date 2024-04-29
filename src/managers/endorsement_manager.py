from src.DAOs.endorsements_DAO import EndorsementDAO
from src.models.pydantic_model import EndorsementCreate
from src.models.posgres_model import Endorsement


class EndorsementManager:
    def __init__(self) -> None:
        self.dao = EndorsementDAO()

    def create(self, endorsement: EndorsementCreate) -> Endorsement:
        return self.dao.create(endorsement)
