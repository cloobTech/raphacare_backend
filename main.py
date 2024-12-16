from models.patient import Patient
from models.medical_practitioner import MedicalPractitioner
from services.consultations.appointment import create_appointment
from storage import DBStorage as DB


import asyncio

db = DB()


async def reload_db():
    """reload"""
    await db.reload()
    print('DB reloaded')

asyncio.run(reload_db())


async def create_appointent():
    """Create a new appointment"""
    x = {
        "patient_id": "7e160edb-3299-4335-8afb-1c2f7fd231a5",
        "medical_practitioner_id": "a99d97fe-f5c3-429e-8a77-46eeab7d4c2c",
        "appointment_start_time": "2023-7-27T02:30:27",
        "appointment_end_time": "2023-8-27T03:30:27",
        "appointment_status": "pending",
        "appointment_reason": "Routine check-up",
        "appointment_note": "Patient requested an early appointment"
    }

    z = await create_appointment(x, db)

    print(z)
asyncio.run(create_appointent())
