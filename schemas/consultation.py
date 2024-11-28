from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Prescription(BaseModel):
    """Prescription Schema"""
    medicine_name: str
    dosage: str
    duration: str
    note: Optional[str] = None


class CreateConsultation(BaseModel):
    """Create Consultation Schema"""
    appointment_id: str
    diagnosis: str
    follow_up_start_date: Optional[datetime] = None
    follow_up_end_date: Optional[datetime] = None
    is_prescription_included: bool = False
    prescriptions: Optional[list[Prescription]] = None
