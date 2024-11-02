import re
import datetime

from databases.schemas import HomeworkGetDTO


def date_match(date: str) -> bool:
    # reg = '^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$'
    reg = '^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)(0[1-9]|1[0-2])(\.|-|/)(0[1-9]|1[0-9]|2[0-9]|3[0-1])$'
    return bool(re.fullmatch(reg, date))


def turn_to_date_type(date: str) -> datetime.date:
    date_split = re.split(r'\.|-|/', date)
    return datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))


def send_all_homework(homework_list: list[HomeworkGetDTO]) -> str:
    message = f'Заданий по предмету {homework_list[0].subject}: {len(homework_list)}\n'
    for i in range(len(homework_list)):
        message += '\n'
        message += f'{i+1}\n'
        date = str(homework_list[i].date)
        status = 'Выполнено' if homework_list[i].finished is True else 'Не выполнено'
        text = homework_list[i].text
        task_id = homework_list[i].id
        message += (f'Срок: {date}\n'
                    f'Статус: {status}\n'
                    f'Задание: {text}\n'
                    f'ID: {task_id}'
                    f'\n')
    return message

