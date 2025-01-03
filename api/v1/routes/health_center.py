from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from services.medical_services.health_centers import (
    update_health_center, delete_health_center, get_health_center_by_id
)


router = APIRouter(tags=['Health Center'],
                   prefix='/api/v1/health_centers')


@router.get('/{health_center_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_health_center_route(health_center_id: str, storage=Depends(get_db_session)):
    """Get Health Center By Id"""
    try:
        health_center = await get_health_center_by_id(health_center_id, storage)
        return health_center
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put('/{health_center_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def update_health_center_route(health_center_id: str, data: dict, storage=Depends(get_db_session)):
    """ Update a health center """
    try:
        health_center = await update_health_center(health_center_id, data, storage)
        return health_center
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete('/{health_center_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def delete_health_center_route(health_center_id: str, storage=Depends(get_db_session)):
    """ Delete a health center """
    try:
        health_center = await delete_health_center(health_center_id, storage)
        return health_center
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
