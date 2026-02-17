from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value
)
from app.services.project_service import get_projects_by_completion_rate


router = APIRouter()


@router.post(
    '/create_report',
    dependencies=[Depends(current_superuser)],
)
async def create_google_sheets_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await get_projects_by_completion_rate(session)
    spreadsheet_url = await create_spreadsheets(wrapper_services)
    await set_user_permissions(settings.spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(
        settings.spreadsheet_id,
        projects,
        wrapper_services
    )
    return {
        'spreadsheet_url': spreadsheet_url
    }
