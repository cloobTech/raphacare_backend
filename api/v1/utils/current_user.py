#!/usr/bin/python3
"""
    Get the current user from the token
"""
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models.user import User
from services.auth.auth_jwt import verify_access_token
import storage


outh2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def get_current_user(token: str = Depends(outh2_scheme)) -> User:
    """Get Current Logged in User"""
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate User token", headers={"WWW-Authenticate": "Bearer"})

    payload: dict = verify_access_token(token, credential_exceptions)
    current_user = await storage.db.get(User, payload.get("user_id"))
    return current_user
