from datetime import datetime
from storage import DBStorage as DB
from models.appointment import Appointment, AppointmentStatus


# format for datetime used within the app
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


async def is_slot_available(storage: DB, data: dict) -> bool:
    """Check if appointment slot is available"""

    med_pract_id = data["medical_practitioner_id"]
    start_time = datetime.strptime(data["appointment_start_time"], TIME_FORMAT)
    end_time = datetime.strptime(data["appointment_end_time"], TIME_FORMAT)

    existing_appointment = await storage.filter(Appointment, Appointment.medical_practitioner_id == med_pract_id, Appointment.appointment_start_time >= start_time, Appointment.appointment_end_time <= end_time, Appointment.appointment_status.in_([AppointmentStatus.pending, AppointmentStatus.confirmed]), fetch_one=True)

    return existing_appointment is None
