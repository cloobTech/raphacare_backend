from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from models.appointment import AppointmentStatus, AppointmentType
from schemas.address import HomeAddressModel


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
    health_center_id: Optional[str] = None
    home_address: Optional[HomeAddressModel] = None

    @model_validator(mode='before')
    @classmethod
    def validate(cls, value: dict):
        """Validate the appointment start and end time"""
        if value.get("appointment_start_time") >= value.get("appointment_end_time"):
            raise ValueError(
                "Appointment end time must be greater than the start time")
        if value.get("appointment_type").lower() == AppointmentType.home_service:
            if not value.get("home_address"):
                raise ValueError(
                    "Home address is required for Home Service appointment")
        elif value.get("appointment_type").lower() == AppointmentType.physical:
            if not value.get("health_center_id"):
                raise ValueError(
                    "Health center Address is required for Physical appointment")
        return value

    @model_validator(mode="before")
    @classmethod
    def validate_appointment(cls, values: dict):
        """Ensure appointment type and status are valid."""
        appointment_type = values.get("appointment_type")
        appointment_status = values.get("appointment_status")

        if not isinstance(appointment_type, AppointmentType):
            raise ValueError(
                f"Invalid appointment type: {appointment_type}. appointment type must be one of {AppointmentType._member_names_}")

        if not isinstance(appointment_status, AppointmentStatus):
            raise ValueError(
                f"Invalid appointment status: {appointment_status}. appointment status must be one of {AppointmentStatus._member_names_}")

        return values


class CreateConsultation(BaseModel):
    """Create Consultation Schema"""
    appointment_id: str
    diagnosis: str
    follow_up_start_date: Optional[datetime] = None
    follow_up_end_date: Optional[datetime] = None
    is_prescription_included: bool = False
    prescriptions: Optional[list[Prescription]] = None
