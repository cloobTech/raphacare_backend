from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage as DB
from models.consultation import Consultation
from models.appointment import Appointment
from schemas.default_response import DefaultResponse
from schemas.consultation import CreateConsultation as CC
from services.consultations.prescription import create_prescription_from_list


async def create_consultation(consultaion_schema_data: CC, storage: DB) -> DefaultResponse:
    """Create consultation"""
    data = consultaion_schema_data.model_dump()
    appointment = await storage.get(Appointment, data['appointment_id'])
    prescription_data: list = data.pop('prescriptions')
    is_prescription_included: bool = data.pop('is_prescription_included')
    if not appointment:
        raise EntityNotFoundError('Appointment not found')
    consultation = Consultation(**data, appointment=appointment)
    if is_prescription_included is True:
        create_prescription_from_list(prescription_data, consultation)
    await storage.merge(consultation)
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
    consultation_data['prescriptions'] = [prescription.to_dict()
                                          for prescription in consultation.prescriptions]
    return DefaultResponse(
        status="success",
        message="Consultation data retrieved successfully",
        data=consultation_data
    )


async def update_consultation(consultation_id: str, consultation_data: dict, storage: DB) -> DefaultResponse:
    """Update consultation"""
    consultation = await storage.get(Consultation, consultation_id)
    if not consultation:
        raise EntityNotFoundError('Consultation object not found')
    if not consultation_data:
        raise DataRequiredError('Data required to update consultation')
    await storage.merge(consultation)
    consultation.update(consultation_data)
    return DefaultResponse(
        status="success",
        message="Consultation updated successfully",
        data=consultation.to_dict()
    )


async def delete_consultation(consultation_id: str, storage: DB) -> DefaultResponse:
    """Delete consultation"""
    consultation = await storage.get(Consultation, consultation_id)
    if not consultation:
        raise EntityNotFoundError('Consultation object not found')
    await storage.merge(consultation)
    await consultation.delete()
    return DefaultResponse(
        status="success",
        message="Consultation deleted successfully"
    )
