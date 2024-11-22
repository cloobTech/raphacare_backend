from typing import Callable, Any
from schemas.default_response import DefaultResponse
from services.auth.internal_auth_management import LocalAuthStrategy
from services.auth.auth_base import AuthStrategy
from storage.database import DBStorage


class AuthContext:
    """
    AuthContext class is responsible for managing the authentication context (register and login users).
    - the idea is to effectively pick the right strategy for the authentication process.
    - the class should be able to switch between different authentication strategies.
    """

    def __init__(self):
        self._strategies = {
            "local": LocalAuthStrategy(),
            # "google": GoogleAuthStrategy(),
            # "facebook": FacebookAuthStrategy(),
        }
        self._strategy: AuthStrategy = None

    def set_strategy(self, strategy_name: str):
        """Set the authentication strategy"""
        if strategy_name not in self._strategies:
            raise ValueError(
                f"Invalid strategy name. Must be one of"
                f" {list(self._strategies.keys())}"
            )
        self._strategy: AuthStrategy = self._strategies.get(strategy_name)

    async def register_user(self, data: dict, storage: DBStorage, email_service: Callable) -> DefaultResponse:
        """register a new user"""
        return await self._strategy.register_user(data, storage, email_service)

    async def login_user(self, login_formdata: Any, storage: DBStorage) -> DefaultResponse:
        """login a user
            :param data: Form data from fastapi request
        """
        # transform the form data to a dictionary
        login_data = {
            'email': login_formdata.username,
            'password': login_formdata.password
        }

        return await self._strategy.login_user(login_data, storage)
