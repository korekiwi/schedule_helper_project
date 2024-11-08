import re
import datetime
import calendar

from databases.schemas import HomeworkGetDTO, ScheduleGetDTO
from databases.models import DayOfWeek


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


def time_match(time: str) -> bool:
    reg = '^([0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])(-)([0-9]|1[0-9]|2[0-3])(:)([0-5][0-9])'
    return bool(re.fullmatch(reg, time))


def split_time(time: str) -> dict:
    time_split = time.split('-')
    first_part = time_split[0].split(':')
    second_part = time_split[1].split(':')
    for i in range(len(first_part)):
        first_part[i] = int(first_part[i])
        second_part[i] = int(second_part[i])
    return {'first_part': first_part, 'second_part': second_part}


def time_check(time: str) -> bool:
    time_dict = split_time(time)
    if (time_dict.get('first_part')[0] > time_dict.get('second_part')[0] or
        (time_dict.get('first_part')[0] == time_dict.get('second_part')[0] and
         time_dict.get('first_part')[1]) > time_dict.get('second_part')[1]):
        return False
    return True


def turn_to_time_type(time: str) -> list[datetime.time]:
    time_dict = split_time(time)
    start = datetime.time(time_dict.get('first_part')[0], time_dict.get('first_part')[1], 0)
    end = datetime.time(time_dict.get('second_part')[0], time_dict.get('second_part')[1], 0)
    return [start, end]


def send_days_of_week(days_list: dict) -> str:
    days = ''
    for i in range(len(days_list)):
        days += str(days_list[i].value.lower())
        if i < len(days_list) - 1:
            days += ', '
    return days


def get_weekday():
    int_day = datetime.datetime.today().weekday()
    days_dict = {0: DayOfWeek.Monday,
                 1: DayOfWeek.Tuesday,
                 2: DayOfWeek.Wednesday,
                 3: DayOfWeek.Thursday,
                 4: DayOfWeek.Friday,
                 5: DayOfWeek.Saturday,
                 6: DayOfWeek.Sunday}
    return days_dict.get(int_day)


def get_time():
    datetime_time = datetime.datetime.today().time()
    hour = int(str(datetime_time)[:2])
    minutes = int(str(datetime_time)[3:5])
    new_datetime_time = datetime.time(hour, minutes, 0)
    return new_datetime_time


def get_tomorrow():
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if ((day == 31 and month in (3, 5, 7, 8, 10, 12))
            or (day == 30 and month in (1, 4, 6, 9, 11))
            or (day == 28 and month == 2 and not calendar.isleap(year))
            or (day == 29 and month == 2)):
        tomorrow_day = 1
    else:
        tomorrow_day = day + 1
    if tomorrow_day == 1 and month == 12:
        tomorrow_year = year + 1
        tomorrow_month = 1
    elif tomorrow_day == 1:
        tomorrow_year = year
        tomorrow_month = month + 1
    else:
        tomorrow_year = year
        tomorrow_month = month
    return datetime.date(tomorrow_year, tomorrow_month, tomorrow_day)


def send_all_schedule(tasks_list: list[ScheduleGetDTO], day: DayOfWeek) -> str:
    message_text = f'{day.value}. Задач: {len(tasks_list)}'
    for i in range(len(tasks_list)):
        message_text += '\n\n' + f'{i + 1}\n'
        message_text += f'{str(tasks_list[i].time_start)[:5]}-{str(tasks_list[i].time_end)[:5]}\n'
        message_text += f'ID: {tasks_list[i].id}\n'
        message_text += tasks_list[i].text
    return message_text


def notify_about_homework(homework: HomeworkGetDTO) -> str:
    text_message = (f'До {homework.date} необходимо выполнить задание по предмету {homework.subject}:\n'
               f'{homework.text}')
    return text_message


def notify_about_task(task: ScheduleGetDTO) -> str:
    text_message = f'{str(task.time_start)[:5]}-{str(task.time_end)[:5]}: {task.text}'
    return text_message

