from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def get_projects_by_completion_rate(session: AsyncSession):
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
