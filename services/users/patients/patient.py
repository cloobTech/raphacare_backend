from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage
from models.patient import Patient
from schemas.user import GetPractionerParams
from services.users.patients.helper import upload_file
from schemas.default_response import DefaultResponse
from utils.update_dict_with_params import update_return_data_with_params


async def get_patient_by_id(patient_id: str, storage: DBStorage, params: GetPractionerParams) -> DefaultResponse:
    """Get patient by id"""
    param_dicts = params.model_dump()

    patient = await storage.get(Patient, patient_id)
    if not patient:
        raise EntityNotFoundError('Patient not found')
    patient_data = patient.to_dict(exclude=['notifications'])
    patient_data['user'] = patient.user.to_dict(
    ) if patient.user else None

    update_return_data_with_params(
        param_dicts, patient_data, patient)

    # include notifications in the return data
    # This line has to come after the update_return_data_with_params function
    if param_dicts.get('get_notifications'):
        patient_data['notifications'] = [notification.to_dict()
                                         for notification in patient.user.notifications]
    return DefaultResponse(
        status="success",
        message="Patient data retrieved successfully",
        data=patient_data
    )


async def get_all_patients(storage: DBStorage) -> DefaultResponse:
    """Get all patients"""
    patients = await storage.all(Patient)
    if not patients:
        return DefaultResponse(
            status="success",
            message="No patients found",
            data=[]
        )
    patients_data = [patient.to_dict() for patient in patients.values()]
    return DefaultResponse(
        status="success",
        message="Patients data retrieved successfully",
        data=patients_data
    )


async def update_patient_info(patient_id: str, data: dict, storage: DBStorage) -> DefaultResponse:
    """Update patient info"""
    patient = await storage.get(Patient, patient_id)
    if not patient:
        raise EntityNotFoundError('Patient not found')
    if len(data) < 1:
        raise DataRequiredError("Data to update is required")
    await storage.merge(patient)
    await patient.update(data)
    return DefaultResponse(
        status="success",
        message="Patient data updated successfully",
        data=patient.to_dict()
    )


async def generic_file_upload(patient_id: str,  resource_type, file, storage) -> DefaultResponse:
    """Generic file upload"""
    upated_patient_data = await upload_file(patient_id,  resource_type, file, storage)
    return DefaultResponse(
        status="success",
        message="File uploaded successfully",
        data=upated_patient_data.to_dict()
    )
