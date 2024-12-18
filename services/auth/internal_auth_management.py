#!/usr/bin/python3
"""Modules to take care of secondary auth functions
    - Register User
    - Verify Email
    - Request Token
    - Reset Password
    - Change Password (Same as reset pwd)
"""

from datetime import datetime, timedelta, timezone
from typing import Callable
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from errors.custome_errors import InvalidTokenError, TokenExpiredError
from models.user import User
from schemas.auth import RegisterUser, RequestResetToken, TokenResponse, VerifyEmailTokenInput
from schemas.default_response import DefaultResponse
from services.auth.auth_base import AuthStrategy
from services.auth.auth_jwt import valid_login
from services.users.user_management import check_user_existence, create_user, create_user_profile
from storage.database import DBStorage
from utils.generate_token import generate_token
from utils.email_service import send_email


class LocalAuthStrategy(AuthStrategy):
    """Local Authentication Strategy"""

    async def login_user(self, data: dict, storage: DBStorage) -> TokenResponse:
        """Login a user"""
        email = data.get('email')
        password = data.get('password')

        token: TokenResponse = await valid_login(email, password, storage)
        return token

    async def register_user(self, data: RegisterUser, storage: DBStorage, background_tasks) -> DefaultResponse:
        """Register a new user"""
        registration_dict = data.model_dump()
        user_auth_details = registration_dict.get('auth_details')
        user_profile_details = registration_dict.get('profile_details')

        # Check if user already exists
        await check_user_existence(storage, user_auth_details.get('email'))
        new_user = create_user(user_auth_details)
        new_user_profile = create_user_profile(new_user, user_profile_details)
        new_user.user_profile_id = new_user_profile.id

        await new_user_profile.save()

        # Send verification email
        # Schedule the email sending task
        background_tasks.add_task(send_email, new_user.email, "Verify your email",
                                  "email_verification.html", {"verification_token": new_user.reset_token})

        return DefaultResponse(
            status="success",
            message="User registered successfully",
            data=new_user_profile.to_dict()
        )

    async def verify_email(self, token_input: VerifyEmailTokenInput, storage: DBStorage) -> TokenResponse:
        """Verify a user's email"""
        token_data = token_input.model_dump()
        token = token_data.get('token')  # verification token (OTP)
        password = token_data['meta'].get('password')

        user = await storage.find_by(User, reset_token=token)
        if not user:
            raise InvalidTokenError("Invalid Token")
        # token is valid for 3 minutes
        if datetime.now(timezone.utc) - user.token_created_at.replace(tzinfo=timezone.utc) > timedelta(minutes=3):
            raise TokenExpiredError("Token Expired")

        # merge the current session object
        await storage.merge(user)

        # update user email_verified status
        await user.update({"email_verified": True, "reset_token": ""})

        token: TokenResponse = await valid_login(user.email, password, storage)
        return token

    async def request_reset_token(self, data: RequestResetToken, storage: DBStorage, email_service: Callable) -> DefaultResponse:
        """Request a reset token"""
        data = data.model_dump()
        email = data.get('email')
        user = await storage.find_by(User, email=email)
        if not user:
            raise NoResultFound("User Not Found!")
        await storage.merge(user)

        # Save the token in your database
        await user.update({"reset_token": generate_token(), "token_created_at": datetime.now(timezone.utc)})

        # REMEMBER TO ADD THIS LINE
        # Send verification email
        await email_service()

        return DefaultResponse(
            status="success",
            message="Token sent successfully"
        )

    async def reset_password(self, data: VerifyEmailTokenInput, storage: DBStorage) -> DefaultResponse:
        """Reset a user's password"""
        data = data.model_dump()
        token = data.get('token')  # otp
        password = data['meta'].get('password')

        user = await storage.find_by(User, reset_token=token)
        if not user:
            raise InvalidTokenError("Invalid Token")
        # tokens valid for 2 minutes
        if datetime.now() - user.token_created_at > timedelta(minutes=3):
            raise TokenExpiredError("Token Expired")

        await storage.merge(user)

        # Update User with hashed password and reset token
        hashed_pwd = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        await user.update({"password": hashed_pwd, "reset_token": ""})

        return DefaultResponse(
            status="success",
            message="Password Reset Successful",
        )
