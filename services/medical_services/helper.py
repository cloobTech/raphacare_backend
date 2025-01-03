from errors.custome_errors import EntityNotFoundError
from models.medical_service import Service
from models.admin import Admin
from models.medical_practitioner import MedicalPractitioner
from storage.database import DBStorage as DB
from schemas.default_response import DefaultResponse


def is_admin(data: dict) -> bool:
    """ Check if user is admin """
    return data.get('is_admin_defined') is True


async def create_service_by_admin(data: dict, storage) -> DefaultResponse:
    """ Create a new service by admin """
    data['approval_status'] = 'approved'
    admin = await storage.get(Admin, data.get('admin_id'))
    if not admin:
        raise EntityNotFoundError('Admin not found')
    await storage.merge(admin)
    service = Service(**data, admin=admin)
    await service.save()
    # create notification
    # notify the whole admin
    return DefaultResponse(
        status="success",
        message="Service created successfully",
        data=service.to_dict()
    )


async def create_service_by_medical_practitioner(data: dict, storage) -> DefaultResponse:
    """ Create a new service by medical practitioner """
    medical_practitioner = await storage.get(MedicalPractitioner, data.get('medical_practitioner_id'))
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    await storage.merge(medical_practitioner)
    service = Service(**data, medical_practitioner=medical_practitioner)
    await service.save()
    # create notification
    # notify the whole admin and the medical_practitioner
    return DefaultResponse(
        status="success",
        message="Service created successfully",
        data=service.to_dict()
    )


async def return_service_by_id(service_id: str, storage: DB) -> Service:
    """ Get a service by id """
    service = await storage.get(Service, service_id)
    return service
