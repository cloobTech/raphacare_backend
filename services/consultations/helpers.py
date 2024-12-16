from storage import DBStorage as DB
from models.appointment import Appointment, AppointmentStatus
from utils.parse_datetime import parse_and_format_datetime


# format for datetime used within the app
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


async def is_slot_available(storage: DB, data: dict) -> bool:
    """Check if appointment slot is available"""

    med_pract_id = data["medical_practitioner_id"]
    start_time = parse_and_format_datetime(data["appointment_start_time"])
    end_time = parse_and_format_datetime(data["appointment_end_time"])

    existing_appointment = await storage.filter(Appointment, Appointment.medical_practitioner_id == med_pract_id, Appointment.appointment_start_time >= start_time, Appointment.appointment_end_time <= end_time, Appointment.appointment_status.in_([AppointmentStatus.pending, AppointmentStatus.confirmed]), fetch_one=True)

    return existing_appointment is None
