from app.infrastructure.database.database import async_seccion_maker
from app.application.entities.bookings.model.bookings_model import Bookings
from sqlalchemy import select, insert

class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_seccion_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_seccion_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get_all(cls, **filter_by):
        async with async_seccion_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_seccion_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()