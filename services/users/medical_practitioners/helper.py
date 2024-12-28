from sqlalchemy import select
from sqlalchemy.orm import selectinload
from errors.custome_errors import EntityNotFoundError
from utils.cloudinary import upload_file_to_cloudinary
from models.medical_practitioner import MedicalPractitioner
from models.health_center import HealthCenter
from schemas.address import HealthCenterModel


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
    async for session in storage.db_session():
        medical_practitioner = await session.execute(
            select(MedicalPractitioner).options(selectinload(MedicalPractitioner.health_centers)).filter(
                MedicalPractitioner.id == medical_practitioner_id)
        )
        medical_practitioner = medical_practitioner.scalars().first()
        if not medical_practitioner:
            raise EntityNotFoundError("Medical Practitioner Not Found")
        return medical_practitioner


def create_health_care_center(data: HealthCenterModel):
    """Create Health Care Center Address"""
    data_dict = data.model_dump()
    center = HealthCenter(**data_dict)
    return center


def format_return_data(data: dict):
    """Format return data"""
    return [center.to_dict() for center in data]
