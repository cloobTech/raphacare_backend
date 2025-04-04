from errors.custome_errors import EntityNotFoundError, DataRequiredError, AppointmentSlotNotAvailableError
from storage import DBStorage as DB
from models.appointment import Appointment
from models.patient import Patient
from models.medical_practitioner import MedicalPractitioner
from schemas.default_response import DefaultResponse
from schemas.consultation import CreateAppointment, GetAppParams
from services.consultations.helpers import is_slot_available, determine_address_type
from services.messaging.notifications.helper import new_pending_appointment, confirmed_rejected_completed_appointment
from utils.update_dict_with_params import update_return_data_with_params


async def get_appointment_by_id(appointment_id: str, storage: DB, params: GetAppParams) -> DefaultResponse:
    """Get appointment by id"""
    param_dicts = params.model_dump()

    appointment = await storage.get(Appointment, appointment_id)
    if not appointment:
        raise EntityNotFoundError('Appointment not found')
    appointment_data = appointment.to_dict()

    update_return_data_with_params(
        param_dicts, appointment_data, appointment)
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
    appointments_data = [appointment.to_dict([
        'patient', 'medical_practitioner', 'address'
    ])
        for appointment in appointments.values()]
    return DefaultResponse(
        status="success",
        message="Appointments data retrieved successfully",
        data=appointments_data
    )


async def create_appointment(data_model: CreateAppointment, storage: DB) -> DefaultResponse:
    """Create appointment"""
    data = data_model.model_dump()
    patient = await storage.get(Patient, data['patient_id'])
    if not patient:
        raise EntityNotFoundError('Patient not found')
    medical_practitioner = await storage.get(MedicalPractitioner, data['medical_practitioner_id'])
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    if not await is_slot_available(storage, data):
        raise AppointmentSlotNotAvailableError("Slot is not available")
    await storage.merge(medical_practitioner)
    await storage.merge(patient)
    appointment = Appointment(**data, patient=patient,
                              medical_practitioner=medical_practitioner)

    # Determine the address type
    appointment = await determine_address_type(appointment, data, storage)
    await appointment.save()
    # Create new pending appointment notification
    await new_pending_appointment(appointment, storage)

    return DefaultResponse(
        status="success",
        message="Appointment created successfully",
        data=appointment.to_dict(
            exclude=['patient', 'medical_practitioner', 'address'])
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
    # Create confirmed/rejected/completed appointment notification
    if 'appointment_status' in data:
        await confirmed_rejected_completed_appointment(appointment, storage)
    return DefaultResponse(
        status="success",
        message="Appointment data updated successfully",
        data=appointment.to_dict(
            [
               'patient', 'medical_practitioner', 'address'
            ]
        )
    )
