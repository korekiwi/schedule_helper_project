from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from databases.db import get_schedule_tasks
from bot.functions import get_weekday, send_all_schedule
from bot.keyboards import days_of_week_view_options
from databases.models import DayOfWeek


schedule_router_show_task = Router()


@schedule_router_show_task.message(Command('show_tasks'))
async def show_tasks(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Посмотреть задачи на:', reply_markup=days_of_week_view_options)


@schedule_router_show_task.callback_query(F.data == 'today')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = get_weekday()
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'mon_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Monday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'tue_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Tuesday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'wed_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Wednesday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'thu_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Thursday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'fri_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Friday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'sat_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Saturday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)


@schedule_router_show_task.callback_query(F.data == 'sun_view')
async def show_today_tasks(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Sunday
    tasks_list = get_schedule_tasks(callback.from_user.id, day)
    message_text = send_all_schedule(tasks_list, day)
    await callback.message.answer(message_text)







