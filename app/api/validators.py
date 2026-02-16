from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


PROJECT_NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден'
PROJECT_CLOSED = 'Закрытый проект нельзя редактировать'
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению'
)
INVALID_FULL_AMOUNT = (
    'Нельзя установить значение full_amount меньше уже вложенной суммы.'
)


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
    exclude_project_id: Optional[int] = None,
) -> None:
    existing_project = await charity_project_crud.get_by_name(
        session, project_name
    )
    if existing_project and (
        exclude_project_id is None
        or existing_project.id != exclude_project_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NAME_DUPLICATE,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(session, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project


async def check_project_not_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get(session, project_id)
    if project and project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_CLOSED
        )


async def check_project_has_no_investments(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get(session, project_id)
    if project and project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS
        )


async def validate_full_amount_update(
    project_id: int,
    new_full_amount: Optional[int],
    session: AsyncSession,
) -> None:
    if new_full_amount is not None:
        project = await charity_project_crud.get(session, project_id)
        if project and new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_FULL_AMOUNT
            )
