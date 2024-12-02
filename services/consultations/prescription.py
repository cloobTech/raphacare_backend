from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage as DB
from models.prescription import Prescription
from models.consultation import Consultation
from schemas.default_response import DefaultResponse


def create_prescription(data: dict, consult: Consultation):
    """Create prescription"""
    data['consultation_id'] = consult.id
    Prescription(**data, consultation=consult)


def create_prescription_from_list(data: list, consultation: Consultation):
    """Create prescription from list"""
    for item in data:
        create_prescription(item, consultation)


async def get_prescription_by_id(prescription_id: str, storage: DB) -> DefaultResponse:
    """Get prescription by id"""
    prescription = await storage.get(Prescription, prescription_id)
    if not prescription:
        raise EntityNotFoundError('Prescription not found')
    prescription_data = prescription.to_dict()
    return DefaultResponse(
        status="success",
        message="Prescription data retrieved successfully",
        data=prescription_data
    )
    

async def update_prescription(prescription_id: str, prescription_data: dict, storage: DB) -> DefaultResponse:
    """Update prescription"""
    prescription = await storage.get(Prescription, prescription_id)
    if not prescription:
        raise EntityNotFoundError('Prescription object not found')
    if not prescription_data:
        raise DataRequiredError('Data required to update prescription')
    storage.merge(prescription)
    prescription.update(prescription_data)
    return DefaultResponse(
        status="success",
        message="Prescription updated successfully",
        data=prescription.to_dict()
    )


async def delete_prescription(prescription_id: str, storage: DB) -> DefaultResponse:
    """Delete prescription"""
    prescription = await storage.get(Prescription, prescription_id)
    if not prescription:
        raise EntityNotFoundError('Prescription object not found')
    storage.merge(prescription)
    await prescription.delete()
    return DefaultResponse(
        status="success",
        message="Prescription deleted successfully"
    )