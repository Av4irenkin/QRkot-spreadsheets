from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value
)
from app.services.project_service import get_projects_by_completion_rate


PROJECTS_NOT_FOUND = 'Нет закрытых проектов для формирования отчета'
REPORT_CREATED = 'Отчёт успешно создан'
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/{}'


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
    if not projects:
        return {'message': PROJECTS_NOT_FOUND}
    spreadsheet_id = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(
        spreadsheet_id,
        projects,
        wrapper_services
    )
    return {
        'message': REPORT_CREATED,
        'spreadsheet_id': spreadsheet_id,
        'spreadsheet_url': SPREADSHEET_URL.format(spreadsheet_id)
    }
