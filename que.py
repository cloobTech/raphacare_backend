import asyncio
from services.events.event_base import ServerSendEvent
from schemas.event import Event
from services.events.event_operations import new_event


async def create_new_appointment():
    """ Create a new appointment """
    e = {
        "type": "appointment",
        "payload": {
            "medical_practitioner_id": "dd5c5e78-2b11-4013-97f6-4e4b5cd4da96",
            "appointment_start_time": "2024-11-27T05:31:27.362490Z",
            "appointment_end_time": "2024-11-27T06:30:27.362490Z",
        }
    }
    event = Event(**e)
    await new_event("12", event)
    await new_event("12", event)

    print(ServerSendEvent.EVENT_QUEUES)


asyncio.run(create_new_appointment())
