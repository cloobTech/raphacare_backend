from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from services.user.medical_practitioner import get_medical_practitioner_by_id, get_all_medical_practitioners, update_medical_practitioner_info


router = APIRouter(tags=['Medical Practitioner'], prefix='/api/v1/medical_practitioners')


@router.get('/{medical_practitioner_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_medical_practitioner_by_id_route(medical_practitioner_id: str, storage=Depends(get_db_session)):
    """Get medical practitioner by id"""
    try:
        medical_practitioner = await get_medical_practitioner_by_id(medical_practitioner_id, storage)
        return medical_practitioner
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_all_medical_practitioners_route(storage=Depends(get_db_session)):
    """Get all medical practitioners"""
    try:
        medical_practitioners = await get_all_medical_practitioners(storage)
        return medical_practitioners
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    

@router.put('/{medical_practitioner_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def update_medical_practitioner_info_route(medical_practitioner_id: str,data: dict, storage=Depends(get_db_session)):
    """Update medical practitioner by id"""
    try:
        medical_practitioner = await update_medical_practitioner_info(medical_practitioner_id, data, storage)
        return medical_practitioner
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e