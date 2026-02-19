from aiogoogle import Aiogoogle
from aiogoogle.excs import HTTPError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value
)


GOOGLE_API_ERROR = 'Ошибка Google API: {}'

router = APIRouter()


@router.post(
    '/create_report',
    dependencies=[Depends(current_superuser)],
)
async def create_google_sheets_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_url = await create_spreadsheets(wrapper_services)
    await set_user_permissions(settings.spreadsheet_id, wrapper_services)
    try:
        await update_spreadsheets_value(
            settings.spreadsheet_id,
            projects,
            wrapper_services
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    except HTTPError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GOOGLE_API_ERROR.format(error)
        )
    return {
        'spreadsheet_url': spreadsheet_url
    }
