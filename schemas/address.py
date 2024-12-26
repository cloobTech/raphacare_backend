from pydantic import BaseModel
from typing import List


class HealthCenterModel(BaseModel):
    """Pydantic Health Center Model"""
    name: str
    address: str
    city: str
    state: str
    postal_code: str | None = None
    medical_practitioner_id: str


class AddHealthCenter(BaseModel):
    """Add Health Center Model"""
    health_centers: List[HealthCenterModel] = []


class HomeAddressModel(BaseModel):
    """Pydantic Home Address Model"""
    street: str
    city: str
    state: str
    postal_code: str | None = None
    appointment_id: str | None = None
