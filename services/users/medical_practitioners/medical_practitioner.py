from sqlalchemy import select
from sqlalchemy.orm import selectinload
from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage
from models.medical_practitioner import MedicalPractitioner
from schemas.default_response import DefaultResponse
from schemas.service import AddServices
from services.medical_services.helper import return_service_by_id
from services.users.medical_practitioners.helper import upload_file


async def get_medical_practitioner_by_id(medical_practitioner_id: str, storage: DBStorage) -> DefaultResponse:
    """Get medical practitioner by id"""
    medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    medical_practitioner_data = medical_practitioner.to_dict()
    medical_practitioner_data['user'] = medical_practitioner.user.to_dict(
    ) if medical_practitioner.user else None
    return DefaultResponse(
        status="success",
        message="Medical practitioner data retrieved successfully",
        data=medical_practitioner_data
    )


async def get_all_medical_practitioners(storage: DBStorage) -> DefaultResponse:
    """Get all medical practitioners"""
    medical_practitioners = await storage.all(MedicalPractitioner)
    if not medical_practitioners:
        return DefaultResponse(
            status="success",
            message="No medical practitioners found",
            data=[]
        )
    medical_practitioners_data = [medical_practitioner.to_dict(
    ) for medical_practitioner in medical_practitioners.values()]
    return DefaultResponse(
        status="success",
        message="Medical practitioners data retrieved successfully",
        data=medical_practitioners_data
    )


async def update_medical_practitioner_info(medical_practitioner_id: str, data: dict, storage: DBStorage) -> DefaultResponse:
    """Update medical practitioner info"""
    medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')
    if len(data) < 1:
        raise DataRequiredError("Data to update is required")
    await storage.merge(medical_practitioner)
    await medical_practitioner.update(data)
    return DefaultResponse(
        status="success",
        message="Medical practitioner data updated successfully",
        data=medical_practitioner.to_dict()
    )


async def add_service_to_medical_practitioner(medical_practitioner_id: str, services_data: AddServices, storage) -> DefaultResponse:
    """ Add a service to a medical practitioner """

    service_list: list = []
    result = []
    data: dict = services_data.model_dump()
    services: list = data.get('services')

    # Step 1: Fetch the medical practitioner and eagerly load the 'services' relationship
    async for session in storage.db_session():  # Ensure session context is open
        medical_practitioner = await session.execute(
            select(MedicalPractitioner).options(selectinload(MedicalPractitioner.services)).filter(
                MedicalPractitioner.id == medical_practitioner_id)
        )
        medical_practitioner = medical_practitioner.scalars().first()

    if not medical_practitioner:
        raise EntityNotFoundError('Medical practitioner not found')

    # Step 2: Loop through each service ID in the request and fetch the service
    for service_id in services:
        service = await return_service_by_id(service_id, storage)
        if service:
            service_list.append(service)
            result.append(service.to_dict())
        else:
            print(f"Service with ID {service_id} not found")

    # Step 3: Append the services to the medical practitioner's services relationship
    medical_practitioner.services.extend(service_list)

    # Step 4: Merge the updated medical practitioner into the session
    async for session in storage.db_session():  # Ensure session context is open
        await session.merge(medical_practitioner)

    # Step 5: Save the changes to the database
    await storage.save()

    return DefaultResponse(
        status="success",
        message="Service(s) added to medical practitioner successfully",
        data=result
    )


# async def add_service_to_medical_practitioner(medical_practitioner_id: str, services_data: AddServices, storage) -> DefaultResponse:
#     """ Add a service to a medical practitioner """

#     print(storage)
#     service_list: list = []
#     data: dict = services_data.model_dump()
#     services: list = data.get('services')
#     medical_practitioner = await storage.get(MedicalPractitioner, medical_practitioner_id)
#     if not medical_practitioner:
#         raise EntityNotFoundError('Medical practitioner not found')
#     for service_id in services:
#         service = await return_service_by_id(service_id, storage)
#         service_list.append(service)
#     medical_practitioner.services.extend(service_list)
#     await storage.merge(medical_practitioner)

#     return DefaultResponse(
#         status="success",
#         message="Service(s) added to medical practitioner successfully",
#         # data=service_list
#     )


async def generic_file_upload(medical_practitioner_id: str,  resource_type, file, storage) -> DefaultResponse:
    """Generic file upload"""
    upated_medical_prac_data = await upload_file(medical_practitioner_id,  resource_type, file, storage)
    return DefaultResponse(
        status="success",
        message="File uploaded successfully",
        data=upated_medical_prac_data.to_dict()
    )
