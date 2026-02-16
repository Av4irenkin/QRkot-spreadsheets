from typing import Generic, Type, TypeVar, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.user import User


ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> Optional[ModelType]:
        return (await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )).scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
        user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in,
        session: AsyncSession,
        commit: bool = True
    ) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
        commit: bool = True
    ) -> ModelType:
        await session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_open_sorted(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        return (await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date.asc())
        )).scalars().all()
