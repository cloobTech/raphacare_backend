from datetime import datetime
import asyncio
from storage.database import DBStorage
from models.user import User, UserType
from models.patient import Patient, Gender
from models.medical_practitioner import PractitionerType, MedicalPractitioner

db = DBStorage()


user_dict = {
    "email": "doctor@example.com",
    "password": "hashed_password",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": UserType.MEDICAL_PRACTITIONER,
    "reset_token": None,
    "token_created_at": None,
    "email_verified": False,
    "disabled": False
}

patient_dict = {
    "user_id": "user_id_value",
    "emergency_contact": "12345568",
    "user_name": "JaneDoe",
    "phone_number": "1234567890",
    "gender": Gender.FEMALE,
    "address": "123 Main St",
    "city": "Anytown",
    "state": "Anystate",
    "country": "Anycountry",
    "date_of_birth": datetime(1990, 1, 1),
}


medical_practitioner_dict = {
    "user_id": "user_id_value",
    "phone_number": "1234567890",
    "practitioner_type": PractitionerType.DOCTOR,
    "specialization": "Cardiology",
    "license_number": "license_number_value",
    "is_verified": False,
    "is_available": True,
    "availability": {"monday": "9am-5pm", "tuesday": "9am-5pm"}
}

async def create_new_medical_practitioner():
    """ Create a new medical practitioner """
    await db.reload()
    practitioner = MedicalPractitioner(**medical_practitioner_dict)
    user = User(**user_dict, medical_practitioner=practitioner)
    await user.save()


# async def create_new_patient():
#     """ Create a new patient """
#     await db.reload()
#     patient = Patient(**patient_dict)
#     user = User(**user_dict, patient=patient)
#     await user.save()


# async def main():
#     """ Main function """
#     await db.reload()
#     user = User(**user_dict)
#     print(user)
#     await user.save()


# asyncio.run(main())
# asyncio.run(create_new_patient())
asyncio.run(create_new_medical_practitioner())
