from pydantic import BaseModel, EmailStr, Field
from schemas.user import AdminProfileDetails, UserAuthDetails, PatientProfileDetails, MedicalPractitionerProfileDetails


class RegisterUser(BaseModel):
    """Register User"""
    auth_details: UserAuthDetails
    profile_details: AdminProfileDetails | PatientProfileDetails | MedicalPractitionerProfileDetails = Field(..., discriminator="user_type")


class TokenResponse(BaseModel):
    """Token Response"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class VerifyEmailTokenInput(BaseModel):
    """Verify Email Token Input"""
    token: str
    meta: dict = {}


class RequestResetToken(BaseModel):
    """Request Reset Token"""
    email: EmailStr
