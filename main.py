from storage import DBStorage as DB
import asyncio


db = DB()

async def reload_db():
    await db.reload()
    print('DB reloaded')


asyncio.run(reload_db())