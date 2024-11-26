from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage
from models.medical_practitioner import MedicalPractitioner
from schemas.default_response import DefaultResponse


async def get_medical_practitioner_by_id(medical_practitioner_id: str, storage: DBStorage) -> DefaultResponse:
    """Get medical practitioner by id"""
    medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    medical_practitioner_data = medical_practitioner.to_dict()
    medical_practitioner_data['user'] = medical_practitioner.user.to_dict(
    ) if medical_practitioner.user else None
    return DefaultResponse(
        status="success",
        message="Medical practitioner data retrieved successfully",
        data=medical_practitioner_data
    )



async def get_all_medical_practitioners(storage: DBStorage) -> DefaultResponse:
    """Get all medical practitioners"""
    medical_practitioners = await storage.all(MedicalPractitioner)
    if not medical_practitioners:
        return DefaultResponse(
            status="success",
            message="No medical practitioners found",
            data=[]
        )
    medical_practitioners_data = [medical_practitioner.to_dict() for medical_practitioner in medical_practitioners.values()]
    return DefaultResponse(
        status="success",
        message="Medical practitioners data retrieved successfully",
        data=medical_practitioners_data
    )



async def update_medical_practitioner_info(medical_practitioner_id: str, data: dict, storage: DBStorage) -> DefaultResponse:
    """Update medical practitioner info"""
    medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    if len(data) < 1:
        raise DataRequiredError("Data to update is required")
    await storage.merge(medical_practitioner)
    await medical_practitioner.update(data)
    return DefaultResponse(
        status="success",
        message="Medical practitioner data updated successfully",
        data=medical_practitioner.to_dict()
    )