from fastapi import APIRouter, HTTPException, status, Request
from sse_starlette.sse import EventSourceResponse
from services.events.event_operations import new_event, stream_events
from schemas.event import Event


router = APIRouter(tags=['Events'], prefix='/api/v1/events')


@router.post('/{user_id}', status_code=status.HTTP_201_CREATED)
async def add_event(user_id: str, event: Event):
    """Add new event"""
    print(event)
    try:
        return await new_event(user_id, event)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/stream/{user_id}', status_code=status.HTTP_200_OK)
async def stream_event(req: Request, user_id: str):
    """Stream events for a specific user."""
    try:
        stream_generator = await stream_events(req, user_id)
        return EventSourceResponse(stream_generator)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
