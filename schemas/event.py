from pydantic import BaseModel, Field


class Event(BaseModel):
    """Service event schema"""
    type: str = Field(..., title="Event type")
    payload: dict = Field(..., title="Event payload")