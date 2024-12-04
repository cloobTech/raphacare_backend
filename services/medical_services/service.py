from errors.custome_errors import EntityNotFoundError, DataRequiredError
from models.medical_service import Service
from storage.database import DBStorage as DB
from schemas.default_response import DefaultResponse
from services.medical_services.helper import (is_admin, create_service_by_admin,
                                              create_service_by_medical_practitioner)


async def create_service(data: dict, storage) -> DefaultResponse:
    """ Create a new service """
    if is_admin(data):
        return await create_service_by_admin(data, storage)
    return await create_service_by_medical_practitioner(data, storage)


async def get_service_by_id(service_id: str, storage: DB) -> DefaultResponse:
    """ Get a service by id """
    service = await storage.get(Service, service_id)
    if not service:
        raise EntityNotFoundError('Service not found')
    service_data = service.to_dict()
    return DefaultResponse(
        status="success",
        message="Service data retrieved successfully",
        data=service_data
    )


async def get_all_services(storage: DB) -> DefaultResponse:
    """ Get all services """
    services = await storage.all(Service)
    if not services:
        return DefaultResponse(
            status="success",
            message="No services found",
            data=[]
        )
    services_data = [service.to_dict()
                     for service in services.values()]
    return DefaultResponse(
        status="success",
        message="Services data retrieved successfully",
        data=services_data
    )


async def update_service(service_id: str, data: dict, storage: DB) -> DefaultResponse:
    """ Update a service """
    service = await storage.get(Service, service_id)
    if not service:
        raise EntityNotFoundError('Service not found')
    if len(data) < 1:
        raise DataRequiredError('Data required for update')
    await storage.merge(service)
    await service.update(data)
    return DefaultResponse(
        status="success",
        message="Service updated successfully",
        data=service.to_dict()
    )


async def delete_service(service_id: str, storage: DB) -> DefaultResponse:
    """ Delete a service """
    service = await storage.get(Service, service_id)
    if not service:
        raise EntityNotFoundError('Service not found')
    await service.delete()
    # create notification
    return DefaultResponse(
        status="success",
        message="Service deleted successfully",
        data=service.to_dict()
    )
