from typing import Callable
from fastapi import APIRouter, Depends,  HTTPException, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth.internal_auth_management import (
    login_user, register_user, verify_email, request_reset_token, reset_password)
from services.auth.auth_google import get_auth_url, get_user_info
from errors.custome_errors import UserDisabledError, EmailNotVerifiedError, UserAlreadyExistsError, InvalidTokenError, TokenExpiredError
from schemas.auth import RegisterUser,  TokenResponse, VerifyEmailTokenInput, RequestResetToken
from schemas.default_response import DefaultResponse
from utils.email_service import send_email
from api.v1.utils.get_db_session import get_db_session
from settings.pydantic_config import settings


router = APIRouter(tags=['Authentication'], prefix='/api/v1/auth')


@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), storage: AsyncSession = Depends(get_db_session)):
    """Handle Logging in a user"""

    try:
        token_dict: TokenResponse = await login_user(user_credentials, storage)
        return token_dict
    except InvalidRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserDisabledError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except EmailNotVerifiedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/google/login',  status_code=status.HTTP_200_OK)
async def google_login():
    """handle google login"""
    try:
        google_auth_url = get_auth_url()
        # RedirectResponse(google_auth_url)
        return google_auth_url
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/google/callback', status_code=status.HTTP_200_OK)
async def google_auth(request: Request,  storage: AsyncSession = Depends(get_db_session)):
    """Handle Google Authentication"""
    try:
        code = request.query_params.get('code')
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code not found in request")
        token_dict: TokenResponse = await get_user_info(code, storage)
        redirect_url = (f"{settings.FRONTEND_URL}/auth?access_token={token_dict.access_token}"
                        "&refresh_token={token_dict.refresh_token}&token_type={token_dict.token_type}")
        return RedirectResponse(url=redirect_url)
    except InvalidRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserDisabledError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except EmailNotVerifiedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def register_new_user(data: RegisterUser, background_task: BackgroundTasks, storage: AsyncSession = Depends(get_db_session)):
    """Register a new user"""
    try:
        response = await register_user(data, storage, background_task)
        return response
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists") from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/verify-email', status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def verify_email_route(token_input: VerifyEmailTokenInput, storage: AsyncSession = Depends(get_db_session)):
    """Verify a user's email"""
    try:
        response = await verify_email(token_input, storage)
        return response
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token Expired") from e
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token") from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/request-reset-token', status_code=status.HTTP_200_OK)
async def request_token(data: RequestResetToken, background_task: BackgroundTasks, storage: AsyncSession = Depends(get_db_session)):
    """Request a reset token"""
    try:
        response = await request_reset_token(data, storage, background_task)
        return response
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found") from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password_route(data: VerifyEmailTokenInput, storage: AsyncSession = Depends(get_db_session)):
    """This route can be used to reset a user's password & (forgot password)"""
    try:
        response = await reset_password(data, storage)
        return response
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token Expired") from e
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token") from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
