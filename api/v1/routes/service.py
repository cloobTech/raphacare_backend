from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from services.medical_services.service import get_service_by_id, delete_service, update_service, get_all_services, create_service


router = APIRouter(tags=['Medical Services'], prefix='/api/v1/services')


@router.get('/{service_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_service_by_id_route(service_id: str, storage=Depends(get_db_session)):
    """Get service by id"""
    try:
        service = await get_service_by_id(service_id, storage)
        return service
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_all_services_route(storage=Depends(get_db_session)):
    """Get all services"""
    try:
        services = await get_all_services(storage)
        return services
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def create_service_route(data: dict, storage=Depends(get_db_session)):
    """Create service"""
    try:
        service = await create_service(data, storage)
        return service
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete('/{service_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def delete_service_route(service_id: str, storage=Depends(get_db_session)):
    """Delete service"""
    try:
        service = await delete_service(service_id, storage)
        return service
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put('/{service_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def update_service_route(service_id: str, service_data: dict, storage=Depends(get_db_session)):
    """Update service"""
    try:
        service = await update_service(service_id, service_data, storage)
        return service
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
