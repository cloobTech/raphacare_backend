from storage import DBStorage as DB

import asyncio

db = DB()


async def reload_db():
    """reload"""
    await db.reload()
    print('DB reloaded')

asyncio.run(reload_db())
