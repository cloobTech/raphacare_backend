from errors.custome_errors import EntityNotFoundError
from storage import DBStorage as DB
from models.consultation import Consultation
from models.appointment import Appointment
from schemas.default_response import DefaultResponse


async def create_consultation(data: dict, storage: DB) -> DefaultResponse:
    """Create consultation"""
    appointment = await storage.get(Appointment, data['appointment_id'])
    if not appointment:
        raise EntityNotFoundError('Appointment not found')
    consultation = Consultation(**data, appointment=appointment)
    await consultation.save()
    return DefaultResponse(
        status="success",
        message="Consultation created successfully",
        data=consultation.to_dict()
    )



async def get_consultation_by_id(consultation_id: str, storage: DB) -> DefaultResponse:
    """Get consultation by id"""
    consultation = await storage.get(Consultation, consultation_id)
    if not consultation:
        raise EntityNotFoundError('Consultation not found')
    consultation_data = consultation.to_dict()
    return DefaultResponse(
        status="success",
        message="Consultation data retrieved successfully",
        data=consultation_data
    )



