from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from schemas.consultation import CreateConsultation as CC
from services.consultations.consultation import create_consultation


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