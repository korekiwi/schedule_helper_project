from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from databases.db import (get_hw_notifications, get_sched_notifications,
                          change_hw_notifications, change_sched_notifications)
from bot.keyboards import hw_notifications_keyboard, sched_notifications_keyboard

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
