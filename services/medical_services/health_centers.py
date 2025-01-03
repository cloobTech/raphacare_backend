from errors.custome_errors import EntityNotFoundError, DataRequiredError
from models.health_center import HealthCenter
from storage.database import DBStorage as DB
from schemas.default_response import DefaultResponse


async def get_health_center_by_id(health_center_id: str, storage: DB) -> DefaultResponse:
    """Get health center by ID"""
    health_center = await storage.get(HealthCenter, health_center_id)
    if not health_center:
        raise EntityNotFoundError('Health center not found')
    return DefaultResponse(
        status="success",
        message="Health center retrieved successfully",
        data=health_center.to_dict()
    )


async def update_health_center(health_center_id: str, data: dict, storage: DB) -> DefaultResponse:
    """ Update a health center """
    health_center = await storage.get(HealthCenter, health_center_id)
    if not health_center:
        raise EntityNotFoundError('Health center not found')
    if len(data) < 1:
        raise DataRequiredError('Data required for update')
    await storage.merge(health_center)
    await health_center.update(data)
    return DefaultResponse(
        status="success",
        message="Health center updated successfully",
        data=health_center.to_dict()
    )


async def delete_health_center(health_center_id: str, storage: DB) -> DefaultResponse:
    """ Delete a health center """
    health_center = await storage.get(HealthCenter, health_center_id)
    if not health_center:
        raise EntityNotFoundError('Health center not found')
    await storage.merge(health_center)
    await health_center.delete()
    return DefaultResponse(
        status="success",
        message="Health center deleted successfully",
        data={}
    )
