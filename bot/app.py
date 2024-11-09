import asyncio
from aiogram import Bot, Dispatcher
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.key import API_TOKEN

from bot.handlers.main_handler import router
from bot.handlers.handler_notifications import notifications_router

from bot.handlers.homework.handler_add import homework_router_add
from bot.handlers.homework.handler_show import homework_router_show
from bot.handlers.homework.handler_delete import homework_router_delete
from bot.handlers.homework.handler_mark import homework_router_mark

from bot.handlers.schedule.handler_add_task import schedule_router_add_task
from bot.handlers.schedule.handler_show_task import schedule_router_show_task
from bot.handlers.schedule.handler_delete_task import schedule_router_delete_task

from bot.handlers.handler_notifications import send_message_homework, send_message_schedule

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    scheduler.add_job(send_message_homework, trigger='cron',
                      hour=14,
                      minute=00,
                      start_date=datetime.datetime.now(),
                      kwargs={'bot': bot})

    scheduler.add_job(send_message_schedule, trigger='interval',
                      seconds=60, kwargs={'bot': bot})

    scheduler.start()

    dp.include_routers(router, notifications_router)
    dp.include_routers(homework_router_add,
                       homework_router_show,
                       homework_router_delete,
                       homework_router_mark)
    dp.include_routers(schedule_router_add_task,
                       schedule_router_show_task,
                       schedule_router_delete_task)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
