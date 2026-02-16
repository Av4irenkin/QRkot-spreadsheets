from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject


FORMAT = '%Y/%m/%d %H:%M:%S'
RANGE = 'A1:G100'
VALUE_INPUT_OPTION = 'USER_ENTERED'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    return settings.spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    pass


async def update_spreadsheets_value(
    spreadsheet_id: str,
    projects: list[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.clear(
            spreadsheetId=spreadsheet_id,
            range=RANGE,
            json={}
        )
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE,
            valueInputOption=VALUE_INPUT_OPTION,
            json={
                'majorDimension': 'ROWS',
                'values': (
                    [
                        ['Отчёт от', datetime.now().strftime(FORMAT)],
                        ['Топ проектов по скорости закрытия'],
                        ['Название проекта', 'Время сбора', 'Описание']
                    ]
                    +
                    [
                        [
                            project.name,
                            str(project.close_date - project.create_date),
                            project.description,
                        ]
                        for project in projects
                        if project.fully_invested
                    ]
                )
            }
        )
    )
