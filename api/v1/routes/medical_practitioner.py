from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile, Body
from errors.custome_errors import EntityNotFoundError, DataRequiredError, InvalidFileError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from schemas.service import AddServices
from schemas.address import HealthCenterModel
from schemas.user import GetPractionerParams
from services.users.medical_practitioners.medical_practitioner import (
    get_medical_practitioner,
    get_all_medical_practitioners, update_medical_practitioner_info, add_service_to_medical_practitioner, add_health_center, generic_file_upload)


router = APIRouter(tags=['Medical Practitioner'],
                   prefix='/api/v1/medical_practitioners')


@router.get('/{medical_practitioner_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_medical_practitioner_by_id_route(medical_practitioner_id: str, storage=Depends(get_db_session), params: GetPractionerParams = Depends()):
    """Get medical practitioner by id"""
    try:
        medical_practitioner = await get_medical_practitioner(medical_practitioner_id, storage=storage, params=params)
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
async def update_medical_practitioner_info_route(medical_practitioner_id: str, data: dict, storage=Depends(get_db_session)):
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


@router.post('/{medical_practitioner_id}/add_service', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def add_service_to_medical_practitioner_route(medical_practitioner_id: str, services_data: AddServices, storage=Depends(get_db_session)):
    """ Add a service to a medical practitioner """
    try:
        medical_practitioner = await add_service_to_medical_practitioner(medical_practitioner_id, services_data, storage)
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


@router.post('/{medical_practitioner_id}/add_health_centers', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def add_health_center_route(medical_practitioner_id: str,  data: list[HealthCenterModel] = Body(...), storage=Depends(get_db_session)):
    """Add Health Center Address"""

    try:
        health_center = await add_health_center(medical_practitioner_id, data, storage)
        return health_center
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post('/{medical_practitioner_id}/upload_file', status_code=status.HTTP_201_CREATED)
async def upload_profile_picture_route(medical_practitioner_id: str,  resource_type: str = Form("profile_picture"), file: UploadFile = File(...), storage=Depends(get_db_session)):
    """Upload profile picture for a medical practitioner"""
    try:
        return await generic_file_upload(medical_practitioner_id, resource_type, file, storage)
    except InvalidFileError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
