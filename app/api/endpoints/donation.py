from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investment import invest_funds

DONATION_CREATE_DESCRIPTION = (
    'Сделать пожертвование.\n\n'
    'Только для зарегистрированных пользователей.'
)
DONATION_CREATE_ERROR = 'Ошибка при создании пожертвования: {}'
DONATION_GET_ALL_DESCRIPTION = (
    'Показать список всех пожертвований.\n\n'
    'Только для суперюзеров.'
)
DONATION_GET_MY_DESCRIPTION = (
    'Показать список пожертвований пользователя, выполняющего запрос.\n\n'
    'Только для зарегистрированных пользователей.'
)


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    description=DONATION_GET_ALL_DESCRIPTION,
    response_model=List[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)]
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    description=DONATION_GET_MY_DESCRIPTION,
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
):
    my_donations = await donation_crud.get_by_user(session, user)
    return my_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    description=DONATION_CREATE_DESCRIPTION
)
async def create_donation(
    donation_in: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
):
    new_donation = await donation_crud.create(
        donation_in,
        session,
        commit=False,
        user=user
    )
    session.add_all(
        invest_funds(
            new_donation,
            await charity_project_crud.get_open_sorted(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
