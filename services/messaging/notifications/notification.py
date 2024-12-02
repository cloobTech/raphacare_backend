from errors.custome_errors import EntityNotFoundError, DataRequiredError
from storage import DBStorage as DB
from models.notification import Notification
from schemas.default_response import DefaultResponse


def create_notification(notification_data: dict, user) -> Notification:
    """Create notification"""
    notification = Notification(**notification_data, user=user)
    return notification


async def get_notification_by_id(notification_id: str, storage: DB) -> DefaultResponse:
    """Get notification by id"""
    notification = await storage.get(Notification, notification_id)
    if not notification:
        raise EntityNotFoundError('Notification not found')
    return DefaultResponse(
        status="success",
        message="Notification found",
        data=notification.to_dict()
    )


async def delete_notification(notification_id: str, storage: DB) -> DefaultResponse:
    """Delete notification"""
    notification = await storage.get(Notification, notification_id)
    if not notification:
        raise EntityNotFoundError('Notification object not found')
    await storage.delete(notification)
    return DefaultResponse(
        status="success",
        message="Notification deleted successfully",
        data=None
    )


async def update_notification(notification_id: str, notification_data: dict, storage: DB) -> DefaultResponse:
    """Update notification"""
    notification = await storage.get(Notification, notification_id)
    if not notification:
        raise EntityNotFoundError('Notification object not found')
    if not notification_data:
        raise DataRequiredError('Data required')
    await storage.merge(notification)
    await notification.update(notification_data)

    return DefaultResponse(
        status="success",
        message="Notification updated successfully",
        data=notification.to_dict()
    )
