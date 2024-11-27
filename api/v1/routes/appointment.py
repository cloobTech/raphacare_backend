from fastapi import APIRouter, Depends, HTTPException, status
from errors.custome_errors import EntityNotFoundError, DataRequiredError, AppointmentSlotNotAvailableError
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from services.consultations.appointment import get_appointment_by_id, get_all_appointments, create_appointment, update_appointment_info


router = APIRouter(tags=['Appointment'], prefix='/api/v1/appointments')


@router.get('/{appointment_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_appointment_by_id_route(appointment_id: str, storage=Depends(get_db_session)):
    """Get appointment by id"""
    try:
        appointment = await get_appointment_by_id(appointment_id, storage)
        return appointment
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    

@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def get_all_appointments_route(storage=Depends(get_db_session)):
    """Get all appointments"""
    try:
        appointments = await get_all_appointments(storage)
        return appointments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DefaultResponse)
async def create_appointment_route(data: dict, storage=Depends(get_db_session)):
    """Create appointment"""
    try:
        appointment = await create_appointment(data, storage)
        return appointment
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AppointmentSlotNotAvailableError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    


@router.put('/{appointment_id}', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def update_appointment_info_route(appointment_id: str,data: dict, storage=Depends(get_db_session)):
    """Update appointment by id"""
    try:
        appointment = await update_appointment_info(appointment_id, data, storage)
        return appointment
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e