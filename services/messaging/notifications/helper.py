from services.messaging.notifications.notification import create_notification
from services.events.event_operations import new_event, convert_dict_to_event
from models.user import User
from models.appointment import Appointment
from storage import DBStorage as DB


async def new_pending_appointment(appointment: Appointment,  storage: DB) -> dict:
    """
    Create new pending appointment notification
    - This notification will be sent to the medical practitioner when a new appointment is pending
    """
    patient_full_name = f"{appointment.patient.first_name} {
        appointment.patient.last_name}"
    notification_data = {
        "user_id": appointment.medical_practitioner.user_id,
        "title": "New Pending Appointment",
        "message": f"New appointment is pending for {patient_full_name}",
        "notification_type": "appointment",
        "is_read": False,
        "resource_id": appointment.id
    }

    user = await storage.get(User, notification_data["user_id"])
    notification = create_notification(notification_data, user)
    await storage.merge(notification)
    await notification.save()
    # Emit new pending appointment event
    event_model = convert_dict_to_event("appointment", notification.to_dict())
    await new_event(user.id, event_model)
    return notification.to_dict()



async def confirmed_rejected_completed_appointment(appointment: Appointment, storage: DB) -> dict:
    """
    Create confirmed/rejected/completed appointment notification
    - This notification will be sent to the patient when the appointment is confirmed/rejected/completed
    """
    await storage.merge(appointment)
    medical_practitioner_full_name = f"{appointment.medical_practitioner.first_name} {
        appointment.medical_practitioner.last_name}"
    notification_data = {
        "user_id": appointment.patient.user_id,
        "title": "Appointment Status",
        "message": f"Your appointment with Dr. {medical_practitioner_full_name} has been {appointment.appointment_status}",
        "notification_type": "appointment",
        "is_read": False,
        "resource_id": appointment.id
    }

    user = await storage.get(User, notification_data["user_id"])
    notification = create_notification(notification_data, user)
    await storage.merge(notification)
    await notification.save()
    # Emit confirmed/rejected/completed appointment event
    event_model = convert_dict_to_event("appointment", notification.to_dict())
    await new_event(user.id, event_model)
    return notification.to_dict()
