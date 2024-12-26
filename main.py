from models.appointment import Appointment
from storage import DBStorage as DB
import asyncio

db = DB()


async def reload_db():
    """reload"""
    await db.drop_all()
    await db.reload()
    print('DB reloaded')

# asyncio.run(reload_db())


async def get_appointment_by_id():
    """Get appointment by id"""
    appointment = await db.get(Appointment, '228d2433-d9cb-41d4-8d1e-a140e7bd2708')
    print(appointment.health_center)
    # if appointment.home_address:
    #     print(appointment.home_address.to_dict())


asyncio.run(get_appointment_by_id())