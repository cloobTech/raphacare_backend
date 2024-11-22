from storage import db


async def get_db_session():
    """Get DB Instance"""
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        await db.shutdown_db()
