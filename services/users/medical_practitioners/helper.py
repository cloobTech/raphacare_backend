from errors.custome_errors import EntityNotFoundError
from utils.cloudinary import upload_file_to_cloudinary
from models.medical_practitioner import MedicalPractitioner


async def upload_file(medical_practitioner_id: str,  resource_type, file, storage, **kwargs):
    """Upload a file to cloudinary."""
    result = await upload_file_to_cloudinary(file)

    secure_url = result.get("secure_url")
    # Update profile picture
    if resource_type == "profile_picture":
        return await update_profile_picture(medical_practitioner_id, secure_url, storage)


async def update_profile_picture(medical_practitioner_id: str, url: str, storage):
    """Update profile picture"""
    medical_practitioner = await get_medical_practitioner_id(medical_practitioner_id, storage)
    await storage.merge(medical_practitioner)
    medical_practitioner.profile_picture_url = url
    await medical_practitioner.save()
    return medical_practitioner


async def get_medical_practitioner_id(medical_practitioner_id: str, storage) -> MedicalPractitioner:
    """Get Medical Practitioner"""
    medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
    if not medical_practitioner:
        raise EntityNotFoundError("Medical Practitioner Not Found")
    return medical_practitioner
