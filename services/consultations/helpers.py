from errors.custome_errors import EntityNotFoundError
from storage import DBStorage as DB
from models.appointment import Appointment, AppointmentStatus
from models.health_center import HealthCenter
from models.address import Address
from utils.parse_datetime import parse_and_format_datetime
from schemas.address import HomeAddressModel


async def is_slot_available(storage: DB, data: dict) -> bool:
    """Check if appointment slot is available"""

    filter_data = {
        "medical_practitioner_id": data['medical_practitioner_id'],
        "appointment_start_time": data['appointment_start_time'],
        "appointment_end_time": data['appointment_end_time']
    }

    med_pract_id = filter_data["medical_practitioner_id"]
    start_time = parse_and_format_datetime(
        filter_data["appointment_start_time"])
    end_time = parse_and_format_datetime(filter_data["appointment_end_time"])

    existing_appointment = await storage.filter(Appointment, Appointment.medical_practitioner_id == med_pract_id, Appointment.appointment_start_time >= start_time, Appointment.appointment_end_time <= end_time, Appointment.appointment_status.in_([AppointmentStatus.pending, AppointmentStatus.confirmed]), fetch_one=True)

    return existing_appointment is None


# check what type of appointment is being created
async def determine_address_type(appointment: Appointment, data: dict, storage: DB) -> Appointment:
    """Determine the address type"""
    if data.get("appointment_type").lower() == "home_service":
        home_address = HomeAddressModel(**data['home_address'])
        home_address.appointment_id = appointment.id
        address = create_appointment_home_address(home_address)
        appointment.address = address
    elif data.get("appointment_type").lower() == "physical":
        health_center_address = await select_health_center(data['health_center_id'], storage)
        await storage.merge(health_center_address)
        appointment.health_center = health_center_address
    return appointment



def create_appointment_home_address(data_model: HomeAddressModel) -> Address:
    """Create Home Address"""
    data = data_model.model_dump()
    address = Address(**data)
    return address


async def select_health_center(health_center_id: str, storage: DB) -> Address:
    """Select health center"""
    health_center = await storage.get(HealthCenter, health_center_id)
    if not health_center:
        raise EntityNotFoundError('Health center not found')
    return health_center
