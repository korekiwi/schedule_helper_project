import datetime

from aiogram import Bot

from databases.db import (get_all_unfinished_homework, get_tg_id_by_user_id,
                          get_schedule_tasks_by_time_start_and_day)
from bot.functions import (turn_to_date_type, notify_about_homework, get_weekday,
                           get_time, notify_about_task)


async def send_message_time(bot: Bot):
    await bot.send_message(1167336636, f'соо через несколько секунд после старта')


# async def send_message_cron(bot: Bot):
#     await bot.send_message(1167336636, f'соо ежедневно в указанное время')


async def send_message_cron(bot: Bot):
    date = turn_to_date_type('2024-11-05')
    all_homework = get_all_unfinished_homework()
    for homework in all_homework:
        tg_id = get_tg_id_by_user_id(homework.user_id)
        text_message = notify_about_homework(homework)
        await bot.send_message(chat_id=int(tg_id), text=text_message)


async def send_message_interval(bot: Bot):
    day = get_weekday()
    time_now = get_time()
    all_tasks = get_schedule_tasks_by_time_start_and_day(day, time_now)
    await bot.send_message(chat_id=1167336636, text=str(all_tasks))
    for task in all_tasks:
        tg_id = get_tg_id_by_user_id(task.user_id)
        text_message = notify_about_task(task)
        await bot.send_message(chat_id=int(tg_id), text=text_message)



# async def send_message_interval(bot: Bot):
#     await bot.send_message(1167336636, f'соо с интервалом в 1 минуту')
