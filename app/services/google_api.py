from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject


FORMAT = '%Y/%m/%d %H:%M:%S'
VALUE_INPUT_OPTION = 'USER_ENTERED'
TABLE_HEADER = [
    ['Отчёт от', '{}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
ROWS_ERROR = 'Недостаточно строк в таблице: нужно {}, доступно {}'
COLUMNS_ERROR = 'Недостаточно колонок в таблице: нужно {}, доступно {}'
RANGE = 'A1:{}'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.get(
            spreadsheetId=settings.spreadsheet_id,
            fields='spreadsheetUrl'
        )
    )
    return response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    pass


async def get_spreadsheet_dimensions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> tuple[int, int]:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.get(
            spreadsheetId=spreadsheet_id,
            fields='sheets.properties.gridProperties'
        )
    )
    sheet_properties = response['sheets'][0]['properties']['gridProperties']
    return sheet_properties['rowCount'], sheet_properties['columnCount']


def _get_column_letter(col_num: int) -> str:
    result = ''
    while col_num > 0:
        col_num -= 1
        result = chr(col_num % 26 + 65) + result
        col_num //= 26
    return result


async def update_spreadsheets_value(
    spreadsheet_id: str,
    projects: list[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    row_count, column_count = await get_spreadsheet_dimensions(
        spreadsheet_id,
        wrapper_services
    )
    all_rows = [
        [row[0], row[1].format(
            datetime.now().strftime(FORMAT)
        )] if i == 0 else row
        for i, row in enumerate(TABLE_HEADER)
    ] + [
        [
            project.name,
            str(project.close_date - project.create_date),
            project.description,
        ]
        for project in projects
    ]
    total_rows = len(all_rows)
    total_cols = max(len(row) for row in all_rows)
    if total_rows > row_count:
        raise ValueError(ROWS_ERROR.format(total_rows, row_count))
    if total_cols > column_count:
        raise ValueError(COLUMNS_ERROR.format(total_cols, column_count))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.clear(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{total_rows}C{total_cols}',
            json={}
        )
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:{_get_column_letter(total_cols)}{total_rows}',
            valueInputOption=VALUE_INPUT_OPTION,
            json={
                'majorDimension': 'ROWS',
                'values': all_rows
            }
        )
    )
