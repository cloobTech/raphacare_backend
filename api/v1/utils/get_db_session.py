from storage import db

async def get_db_session():
    """Get DB Instance"""
    try:
        print('DB Session')
        yield db
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        print('Shutting down DB')
        await db.shutdown_db()



async def db_session():
    """Get DB Instance"""
    try:
        print('Session')
        yield db.db_session()
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        print('Shutting down DB')
        await db.shutdown_db()
