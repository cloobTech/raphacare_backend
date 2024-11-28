from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from services.consultations.prescription import get_prescription_by_id, update_prescription, delete_prescription


router = APIRouter(tags=['Prescription'], prefix='/api/v1/prescriptions')


@router.get('/{prescription_id}', response_model=DefaultResponse)
async def get_prescription_by_id_route(prescription_id: str, storage=Depends(get_db_session)):
    """Get prescription by id"""
    try:
        prescription = await get_prescription_by_id(prescription_id, storage)
        return prescription
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    

@router.put('/{prescription_id}', response_model=DefaultResponse)
async def update_prescription_route(prescription_id: str, data: dict, storage=Depends(get_db_session)):
    """Update prescription"""
    try:
        prescription = await update_prescription(prescription_id, data, storage)
        return prescription
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    

@router.delete('/{prescription_id}', response_model=DefaultResponse)
async def delete_prescription_route(prescription_id: str, storage=Depends(get_db_session)):
    """Delete prescription"""
    try:
        prescription = await delete_prescription(prescription_id, storage)
        return prescription
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

