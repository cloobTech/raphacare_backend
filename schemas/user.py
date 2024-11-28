from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from models.medical_practitioner import PractitionerType
from models.patient import Gender
from typing import Literal, Optional


class UserType(str, Enum):
    """User Type Enum"""
    admin = 'admin'
    medical_practitioner = 'medical_practitioner'
    patient = 'patient'


class UserAuthDetails(BaseModel):
    """User Authentication Details"""
    email: EmailStr
    password: str | None = Field(None, min_length=6, max_length=20)
    user_type: UserType
    reset_token: str | None = ""
    token_created_at: datetime | None = None
    email_verified: bool = False
    disabled: bool = False
    user_profile_id: str | None = None
    auth_type: str = "local"

    class Config:
        use_enum_values = True


class AdminProfileDetails(BaseModel):
    first_name: str
    last_name: str
    other_names: str | None = None
    type: str | None = None
    user_type: Literal['admin'] = 'admin'

    class Config:
        use_enum_values = True


class MedicalPractitionerProfileDetails(BaseModel):
    first_name: str
    last_name: str
    other_names: str | None = None
    phone_number: str | None = None
    practitioner_type: PractitionerType | None = None
    specialization: str | None = None
    license_number: str | None = None
    is_verified: bool = False
    availability: dict | None = None
    is_available: bool = True
    user_type: Literal['medical_practitioner'] = 'medical_practitioner'

    class Config:
        use_enum_values = True


class PatientProfileDetails(BaseModel):
    first_name: str = Field(..., max_length=60)
    last_name: str = Field(..., max_length=60)
    other_names: Optional[str] = Field(None, max_length=60)
    user_name: Optional[str] = Field(None, max_length=60)
    emergency_contact: Optional[str] = Field(None, max_length=60)
    phone_number: Optional[str] = Field(None, max_length=60)
    gender: Optional[Gender] = None
    address: Optional[str] = Field(None, max_length=60)
    city: Optional[str] = Field(None, max_length=60)
    state: Optional[str] = Field(None, max_length=60)
    country: Optional[str] = Field(None, max_length=60)
    date_of_birth: Optional[datetime] = None
    user_type: Literal['patient'] = 'patient'

    class Config:
        use_enum_values = True
