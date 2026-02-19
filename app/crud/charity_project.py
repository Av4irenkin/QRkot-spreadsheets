from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase[CharityProject]):

    async def get_by_name(
        self,
        session: AsyncSession,
        project_name: str,
    ) -> Optional[CharityProject]:
        return (await session.execute(
            select(CharityProject).where(CharityProject.name == project_name)
        )).scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        days_diff = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        ).label('days_diff')
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(True))
            .order_by(days_diff.asc())
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
