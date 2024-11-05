import datetime

from aiogram import Bot

from databases.db import get_all_homework, get_tg_id_by_user_id


async def send_message_time(bot: Bot):
    await bot.send_message(1167336636, f'соо через несколько секунд после старта')


# async def send_message_cron(bot: Bot):
#     await bot.send_message(1167336636, f'соо ежедневно в указанное время')


async def send_message_cron(bot: Bot):
    all_homework = get_all_homework(datetime.date.today())
    # for homework in all_homework:
    #     tg_id = get_tg_id_by_user_id(homework.user_id)
    #     await bot.send_message(tg_id, str(homework))
    await bot.send_message(1167336636, str(all_homework))


async def send_message_interval(bot: Bot):
    await bot.send_message(1167336636, f'соо с интервалом в 1 минуту')
