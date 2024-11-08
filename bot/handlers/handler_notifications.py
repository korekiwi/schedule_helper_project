from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from databases.db import (get_hw_notifications, get_sched_notifications,
                          change_hw_notifications, change_sched_notifications,
                          get_all_unfinished_homework, get_tg_id_by_user_id,
                          get_schedule_tasks_by_time_start_and_day)
from bot.keyboards import hw_notifications_keyboard, sched_notifications_keyboard
from bot.functions import (notify_about_homework, get_weekday,
                           get_time, notify_about_task)

notifications_router = Router()

"""ДЗ"""


@notifications_router.message(Command('hw_notifications'))
async def view_hw_notifications(message: Message, state: FSMContext):
    await state.clear()
    notifications = get_hw_notifications(message.from_user.id)
    turned = 'включены' if notifications else 'выключены'
    await message.answer(text=f'Уведомления о выполнении ДЗ {turned}',
                         reply_markup=hw_notifications_keyboard)


@notifications_router.callback_query(F.data == 'hw_turn_on')
async def view_hw_notifications(callback: CallbackQuery, state: FSMContext):
    notifications = get_hw_notifications(callback.from_user.id)
    if notifications:
        await callback.message.answer('Уведомления уже включены.')
    else:
        change_hw_notifications(callback.from_user.id, 1)
        await callback.message.answer('Уведомления включены.')


@notifications_router.callback_query(F.data == 'hw_turn_off')
async def view_hw_notifications(callback: CallbackQuery, state: FSMContext):
    notifications = get_hw_notifications(callback.from_user.id)
    if not notifications:
        await callback.message.answer('Уведомления уже выключены.')
    else:
        change_hw_notifications(callback.from_user.id, 0)
        await callback.message.answer('Уведомления выключены.')


async def send_message_homework(bot: Bot):
    all_homework = get_all_unfinished_homework()
    for homework in all_homework:
        tg_id = get_tg_id_by_user_id(homework.user_id)
        text_message = notify_about_homework(homework)
        await bot.send_message(chat_id=int(tg_id), text=text_message)


"""Расписание"""


@notifications_router.message(Command('sched_notifications'))
async def view_schedule_notifications(message: Message, state: FSMContext):
    await state.clear()
    notifications = get_sched_notifications(message.from_user.id)
    turned = 'включены' if notifications else 'выключены'
    await message.answer(text=f'Уведомления о задачах {turned}',
                         reply_markup=sched_notifications_keyboard)


@notifications_router.callback_query(F.data == 'sched_turn_on')
async def view_hw_notifications(callback: CallbackQuery, state: FSMContext):
    notifications = get_sched_notifications(callback.from_user.id)
    if notifications:
        await callback.message.answer('Уведомления уже включены.')
    else:
        change_sched_notifications(callback.from_user.id, 1)
        await callback.message.answer('Уведомления включены.')


@notifications_router.callback_query(F.data == 'sched_turn_off')
async def view_hw_notifications(callback: CallbackQuery, state: FSMContext):
    notifications = get_sched_notifications(callback.from_user.id)
    if not notifications:
        await callback.message.answer('Уведомления уже выключены.')
    else:
        change_sched_notifications(callback.from_user.id, 0)
        await callback.message.answer('Уведомления выключены.')


async def send_message_schedule(bot: Bot):
    day = get_weekday()
    time_now = get_time()
    all_tasks = get_schedule_tasks_by_time_start_and_day(day, time_now)
    for task in all_tasks:
        tg_id = get_tg_id_by_user_id(task.user_id)
        text_message = notify_about_task(task)
        await bot.send_message(chat_id=int(tg_id), text=text_message)
