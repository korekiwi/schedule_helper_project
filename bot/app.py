import asyncio
from aiogram import Bot, Dispatcher

from key import API_TOKEN

from bot.handlers.main_handler import router

from bot.handlers.homework.handler_add import homework_router_add
from bot.handlers.homework.handler_show import homework_router_show
from bot.handlers.homework.handler_delete import homework_router_delete
from bot.handlers.homework.handler_mark import homework_router_mark


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(homework_router_add)
    dp.include_router(homework_router_show)
    dp.include_router(homework_router_delete)
    dp.include_router(homework_router_mark)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
