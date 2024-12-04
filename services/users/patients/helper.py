from errors.custome_errors import EntityNotFoundError
from utils.cloudinary import upload_file_to_cloudinary
from models.patient import Patient



async def upload_file(patient_id: str,  resource_type, file, storage, **kwargs):
    """Upload a file to cloudinary."""
    result = await upload_file_to_cloudinary(file)

    secure_url = result.get("secure_url")
    # Update profile picture
    if resource_type == "profile_picture":
        return await update_profile_picture(patient_id, secure_url, storage)
    


async def update_profile_picture(patient_id: str, url: str, storage):
    """Update profile picture"""
    patient = await get_patient_id(patient_id, storage)
    await storage.merge(patient)
    patient.profile_picture_url = url
    await patient.save()
    return patient



async def get_patient_id(patient_id: str, storage) -> Patient:
    """Get Patient"""
    patient = await storage.get(Patient, patient_id)
    if not patient:
        raise EntityNotFoundError("Patient Not Found")
    return patient