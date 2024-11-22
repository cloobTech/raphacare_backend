from abc import ABC, abstractmethod
from typing import Callable
from schemas.default_response import DefaultResponse
from storage.database import DBStorage


class AuthStrategy(ABC):
    """Abstract class for authentication strategies"""
    @abstractmethod
    async def register_user(self, data: dict, storage: DBStorage, email_service: Callable) -> DefaultResponse:
        """register a new user"""

    @abstractmethod
    async def login_user(self, data: dict, storage: DBStorage) -> DefaultResponse:
        """login a user"""
