from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from models.appointment import AppointmentStatus, AppointmentType


class Prescription(BaseModel):
    """Prescription Schema"""
    medicine_name: str
    dosage: str
    duration: str
    note: Optional[str] = None


class CreateAppointment(BaseModel):
    """Create appointment schema"""
    patient_id: str = Field(..., title="Patient ID")
    medical_practitioner_id: str = Field(..., title="Medical Practitioner ID")
    appointment_start_time: str = Field(..., title="Appointment Start Time")
    appointment_end_time: str = Field(..., title="Appointment End Time")
    appointment_status: str = Field(
        AppointmentStatus.pending, title="Appointment Staus")
    appointment_type: str = Field(
        AppointmentType.online, title="Appointment Type")
    appointment_reason: str = Field(..., title="Appointment Reason")
    appointment_note: str = Field(None, title="Appointment Note")


class CreateConsultation(BaseModel):
    """Create Consultation Schema"""
    appointment_id: str
    diagnosis: str
    follow_up_start_date: Optional[datetime] = None
    follow_up_end_date: Optional[datetime] = None
    is_prescription_included: bool = False
    prescriptions: Optional[list[Prescription]] = None
