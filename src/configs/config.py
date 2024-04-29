from src.models.pydantic_model import Configuration
import os


class ConfigurationManager:
    def __init__(self) -> None:
        self.configuration = Configuration(
            POSTGRES_DATABASE_URL_CONNECTION_STRING=os.environ.get(
                "POSTGRES_DATABASE_URL_CONNECTION_STRING"
            )
        )

    def get_configuration(self) -> Configuration:
        return self.configuration


manager = ConfigurationManager()
CONFIG = manager.get_configuration()
