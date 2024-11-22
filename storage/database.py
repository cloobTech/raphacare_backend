from typing import AsyncGenerator, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.sql.expression import BinaryExpression
from models import user, patient, medical_history, medical_practitioner, admin
from models.base_model import Base


class DBStorage:
    """ Database storage class """

    MODELS = {
        "User": user.User,
        "Patient": patient.Patient,
        "MedicalPractitioner": medical_practitioner.MedicalPractitioner,
        "MedicalHistory": medical_history.MedicalHistory,
        "Admin": admin.Admin

    }

    __engine = None

    def __init__(self, db_uri: str = 'sqlite+aiosqlite:///db.sqlite3'):
        """ Initialize the database storage class """

        self.__engine = create_async_engine(db_uri, echo=False)
        self.__session_maker = async_sessionmaker(
            self.__engine, expire_on_commit=False)

    async def _session(self) -> AsyncGenerator[AsyncSession, None]:
        """Create and return a session object"""
        async with self.__session_maker() as session:
            async with session.begin():
                yield session

    async def reload(self):
        """Reload the database schema"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        """Drop all tables in the database"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def new(self, obj: Type[Base]):
        """Add objects to the current database session"""
        async for session in self._session():
            session.add(obj)

    async def save(self):
        """Commit all changes of the current database session"""
        async for session in self._session():
            await session.commit()

    async def delete(self, obj: Type[Base | None] = None):
        """Delete an object from the current database session if not None"""
        if obj:
            async for session in self._session():
                await session.delete(obj)
                await self.save()

    async def find_by(self, cls: Type[Base], **kwargs: Any) -> Type[Base] | None:
        """retrieves one object based on a class name and kwargs (class attribute)"""
        async for session in self._session():
            query_result = await session.execute(select(cls).filter_by(**kwargs))
            result = query_result.scalars().first()
            if result:
                return result
        return None

    async def filter(self, cls: Type[Base], *args: BinaryExpression) -> dict:
        """retrieves all objects based on a class name and kwargs (class attribute)"""
        objects = {}
        async for session in self._session():
            query_result = await session.execute(select(cls).filter(*args))
            result = query_result.scalars().all()
            for obj in result:
                obj_reference = f'{type(obj).__name__}.{obj.id}'
                objects[obj_reference] = obj
        return objects

    async def shutdown_db(self):
        """Close current DB session"""
        async for session in self._session():
            await session.close()

    async def rollback(self):
        """Roll back current DB session"""
        async for session in self._session():
            await session.rollback()

    async def merge(self, obj: Type[Base]):
        """Merge the current session with the object"""
        async for session in self._session():
            merged_obj = await session.merge(obj)
            return merged_obj

    async def all(self, cls: Type[Base] | None = None) -> dict:
        """Query on the current database session all objects"""
        objects = {}
        if cls is not None:
            try:
                async for session in self._session():
                    result = await session.execute(select(cls))
                    result = result.scalars().all()
                    for obj in result:
                        obj_reference = f'{type(obj).__name__}.{obj.id}'
                        objects[obj_reference] = obj
                    return objects
            except Exception:
                pass
        else:
            for model in self.MODELS.values():
                async for session in self._session():
                    result = await session.execute(select(model))
                    result = result.scalars().all()
                    for obj in result:
                        obj_reference = f'{type(obj).__name__}.{obj.id}'
                        objects[obj_reference] = obj
            return objects

    async def get(self, cls: Type[Base], obj_id: str) -> dict | None:
        """retrieves one object based on a class name and obj_id"""
        if cls and obj_id:
            dict_key = f'{cls.__name__}.{obj_id}'
            all_obj = await self.all(cls)
            return all_obj.get(dict_key)
        return None

    def count(self, cls: Type[Base] | None = None) -> int:
        """Return the count of all objects in storage"""
        return (len(self.all(cls)))
