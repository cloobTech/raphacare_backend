from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from schemas.consultation import CreateConsultation as CC
from services.consultations.consultation import create_consultation, get_consultation_by_id, update_consultation, delete_consultation


router = APIRouter(tags=['Consultation'], prefix='/api/v1/consultations')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def create_consultation_route(data: CC, storage=Depends(get_db_session)):
    """Create consultation"""
    try:
        consultation = await create_consultation(data, storage)
        return consultation
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.get('/{consultation_id}', response_model=DefaultResponse)
async def get_consultation_by_id_route(consultation_id: str, storage=Depends(get_db_session)):
    """Get consultation by id"""
    try:
        consultation = await get_consultation_by_id(consultation_id, storage)
        return consultation
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.put('/{consultation_id}', response_model=DefaultResponse)
async def update_consultation_route(consultation_id: str, data: dict, storage=Depends(get_db_session)):
    """Update consultation"""
    try:
        consultation = await update_consultation(consultation_id, data, storage)
        return consultation
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.delete('/{consultation_id}', response_model=DefaultResponse)
async def delete_consultation_route(consultation_id: str, storage=Depends(get_db_session)):
    """Delete consultation"""
    try:
        consultation = await delete_consultation(consultation_id, storage)
        return consultation
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e