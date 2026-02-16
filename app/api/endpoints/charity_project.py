from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_exists,
    check_project_name_duplicate,
    check_project_not_closed,
    check_project_has_no_investments,
    validate_full_amount_update
)
from app.api.responses import (
    CHARITY_PROJECT_CREATE_EXTRA_RESPONSES,
    CHARITY_PROJECT_UPDATE_EXTRA_RESPONSES,
    CHARITY_PROJECT_DELETE_EXTRA_RESPONSES
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investment import invest_funds


PROJECT_GET_ALL_DESCRIPTION = 'Показать список всех целевых проектов.'
PROJECT_CREATE_DESCRIPTION = (
    'Создать целевой проект.\n\n'
    'Только для суперюзеров.'
)
PROJECT_UPDATE_DESCRIPTION = (
    'Редактировать целевой проект.\n\n'
    'Только для суперюзеров.\n\n'
    'Закрытый проект нельзя редактировать;'
    ' нельзя установить требуемую сумму меньше уже вложенной.'
)
PROJECT_DELETE_DESCRIPTION = (
    'Удалить целевой проект.\n\n'
    'Только для суперюзеров.\n\n'
    'Нельзя удалить проект, в который уже были инвестированы средства.'
)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    description=PROJECT_GET_ALL_DESCRIPTION,
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(session: SessionDep):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    responses=CHARITY_PROJECT_CREATE_EXTRA_RESPONSES,
    description=PROJECT_CREATE_DESCRIPTION
)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)]
):
    await check_project_name_duplicate(project_in.name, session)
    new_project = await charity_project_crud.create(
        project_in,
        session,
        commit=False
    )
    session.add_all(
        invest_funds(
            new_project,
            await donation_crud.get_open_sorted(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    responses=CHARITY_PROJECT_UPDATE_EXTRA_RESPONSES,
    description=PROJECT_UPDATE_DESCRIPTION
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)]
):
    project = await check_project_exists(project_id, session)
    await check_project_not_closed(project_id, session)
    if project_in.name is not None and project_in.name != project.name:
        await check_project_name_duplicate(
            project_in.name,
            session,
            project_id
        )
    await validate_full_amount_update(
        project_id,
        project_in.full_amount,
        session
    )
    updated_project = await charity_project_crud.update(
        project, project_in, session, commit=False
    )
    updated_project.close_if_fully_invested()
    session.add_all(
        invest_funds(
            updated_project,
            await donation_crud.get_open_sorted(session)
        )
    )
    await session.commit()
    await session.refresh(updated_project)
    return updated_project


@router.delete(
    '/{project_id}',
    description=PROJECT_DELETE_DESCRIPTION,
    response_model=CharityProjectDB,
    responses=CHARITY_PROJECT_DELETE_EXTRA_RESPONSES
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)]
):
    project = await check_project_exists(project_id, session)
    await check_project_has_no_investments(project_id, session)
    deleted_project = await charity_project_crud.remove(project, session)
    return deleted_project
