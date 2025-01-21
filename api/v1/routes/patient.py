from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from errors.custome_errors import EntityNotFoundError, DataRequiredError, InvalidFileError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from schemas.user import GetPractionerParams
from services.users.patients.patient import get_patient_by_id, get_all_patients, update_patient_info, generic_file_upload


router = APIRouter(tags=['Patient'], prefix='/api/v1/patients')


@router.get('/{patient_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_patient_by_id_route(patient_id: str, storage=Depends(get_db_session), params: GetPractionerParams = Depends()):
    """Get patient by id"""
    try:
        patient = await get_patient_by_id(patient_id, storage, params=params)
        return patient
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_all_patients_route(storage=Depends(get_db_session)):
    """Get all patients"""
    try:
        patients = await get_all_patients(storage)
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put('/{patient_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def update_patient_info_route(patient_id: str, data: dict, storage=Depends(get_db_session)):
    """Update patient by id"""
    try:
        patient = await update_patient_info(patient_id, data, storage)
        return patient
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/{patient_id}/upload_file', status_code=status.HTTP_201_CREATED)
async def upload_profile_picture_route(patient_id: str,  resource_type: str = Form("profile_picture"), file: UploadFile = File(...), storage=Depends(get_db_session)):
    """Upload profile picture for a medical practitioner"""
    try:
        return await generic_file_upload(patient_id, resource_type, file, storage)
    except InvalidFileError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
