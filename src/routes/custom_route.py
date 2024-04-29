from fastapi import APIRouter
from src.errors.handle_exceptions import handle_exceptions


class CustomAPIRouter(APIRouter):
    def add_api_route(self, path: str, endpoint, **kwargs):
        super().add_api_route(path, handle_exceptions(endpoint), **kwargs)
