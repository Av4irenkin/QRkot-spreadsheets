from typing import Optional

from sqlalchemy import select
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


charity_project_crud = CRUDCharityProject(CharityProject)
