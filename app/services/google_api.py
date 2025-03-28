from datetime import datetime, timedelta
from operator import itemgetter

from aiogoogle import Aiogoogle

from app.core.config import settings


API_ERROR = 'Ошибка при обращении к Google API: {e}'
ROW_NUMBER = 100
COLUMN_NUMBER = 10
TABLE_LENGTH_ERROR = (
    'Таблица больше доступного места!'
    'Размер этой таблицы: {rows_needed}x{columns_needed}, '
    'доступный размер: {ROW_NUMBER}x{COLUMN_NUMBER}'
)
FORMAT = '%Y/%m/%d %H:%M:%S'
REPORT_HEAD = 'Отчёт от {date}'
SPREADHSEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_NUMBER,
            columnCount=COLUMN_NUMBER,
        )
    ))]
)
TABLE_HEAD = [
    ['Отчёт от', '{date}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADHSEET_BODY.copy()
    spreadsheet_body['properties']['title'] = (
        REPORT_HEAD.format(date=datetime.now().strftime(FORMAT)))
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    sorted_projects = []
    for project in projects:
        name, close_date, create_date, description = project
        total_seconds = (create_date - close_date).total_seconds()
        days = int(total_seconds // (24 * 3600))
        total_seconds %= (24 * 3600)
        hours = int(total_seconds // 3600)
        total_seconds %= 3600
        minutes = int(total_seconds // 60)
        total_seconds %= 60
        seconds = int(total_seconds)
        duration_str = str(timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds))
        sorted_projects.append({
            'name': name,
            'duration': duration_str,
            'description': description,
            'total_seconds': total_seconds
        })
    sorted_projects.sort(key=itemgetter('total_seconds'))
    table_head = TABLE_HEAD.copy()
    table_head[1][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_head,
        *[list(map(
            str, [project['name'], project['duration'], project['description']]
        )) for project in sorted_projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    rows_needed = len(table_values)
    columns_needed = max(
        len(row) for row in table_values) if rows_needed > 0 else 0
    if rows_needed > ROW_NUMBER or columns_needed > COLUMN_NUMBER:
        raise ValueError(TABLE_LENGTH_ERROR.format(
            rows_needed=rows_needed,
            columns_needed=columns_needed,
            ROW_NUMBER=ROW_NUMBER,
            COLUMN_NUMBER=COLUMN_NUMBER
        ))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='R1C1:R{rows_needed}C{columns_needed}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )