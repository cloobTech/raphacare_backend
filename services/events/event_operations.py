import asyncio
from services.events.event_base import ServerSendEvent
from schemas.event import Event


async def new_event(user_id: str, event: Event):
    """Add new event to the queue"""
    ServerSendEvent.add_event(user_id, event)
    return {"message": "Event added to the queue"}


async def stream_events(req, user_id: str):
    """Stream events for a specific user."""

    async def stream_generator():
        while True:
            if await req.is_disconnected():
                print(f"Client {user_id} disconnected")
                break

            event = ServerSendEvent.get_event(user_id)
            if event:
                yield {
                    "data": event.model_dump(),
                    # Serialize the event model
                    "event":  event.model_dump()['type'],
                }
            await asyncio.sleep(1)  # Prevent busy-waiting

    return stream_generator()


def convert_dict_to_event(event_type: str, data: dict) -> Event:
    """Convert dictionary to Event model"""

    return Event(
        type=event_type,
        payload=data
    )
