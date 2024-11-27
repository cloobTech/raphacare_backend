from errors.custome_errors import EntityNotFoundError, DataRequiredError, AppointmentSlotNotAvailableError
from storage import DBStorage as DB
from models.appointment import Appointment
from models.patient import Patient
from models.medical_practitioner import MedicalPractitioner
from schemas.default_response import DefaultResponse
from services.consultations.helpers import is_slot_available


async def get_appointment_by_id(appointment_id: str, storage: DB) -> DefaultResponse:
    """Get appointment by id"""
    appointment = await storage.get(Appointment, appointment_id)
    if not appointment:
        raise EntityNotFoundError('Appointment not found')
    appointment_data = appointment.to_dict()
    return DefaultResponse(
        status="success",
        message="Appointment data retrieved successfully",
        data=appointment_data
    )


async def get_all_appointments(storage: DB) -> DefaultResponse:
    """Get all appointments"""
    appointments = await storage.all(Appointment)
    if not appointments:
        return DefaultResponse(
            status="success",
            message="No appointments found",
            data=[]
        )
    appointments_data = [appointment.to_dict()
                         for appointment in appointments.values()]
    return DefaultResponse(
        status="success",
        message="Appointments data retrieved successfully",
        data=appointments_data
    )


async def create_appointment(data: dict, storage: DB) -> DefaultResponse:
    """Create appointment"""
    patient = await storage.get(Patient, data['patient_id'])
    if not patient:
        raise EntityNotFoundError('Patient not found')
    medical_practitioner = await storage.get(MedicalPractitioner, data['medical_practitioner_id'])
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    filter_data = {
        "medical_practitioner_id": data['medical_practitioner_id'],
        "appointment_start_time": data['appointment_start_time'],
        "appointment_end_time": data['appointment_end_time']
    }
    if not await is_slot_available(storage, filter_data):
        raise AppointmentSlotNotAvailableError("Slot is not available")
    await storage.merge(medical_practitioner)
    await storage.merge(patient)
    appointment = Appointment(**data, patient=patient,
                              medical_practitioner=medical_practitioner)
    await appointment.save()
    return DefaultResponse(
        status="success",
        message="Appointment created successfully",
        data=appointment.to_dict()
    )


async def update_appointment_info(appointment_id: str, data: dict, storage: DB) -> DefaultResponse:
    """Update appointment info"""
    appointment = await storage.get(Appointment, appointment_id)
    if not appointment:
        raise EntityNotFoundError('Appointment not found')
    if len(data) < 1:
        raise DataRequiredError("Data to update is required")
    await storage.merge(appointment)
    await appointment.update(data)
    return DefaultResponse(
        status="success",
        message="Appointment data updated successfully",
        data=appointment.to_dict()
    )
