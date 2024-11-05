from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from databases.models import DayOfWeek
from databases.db import create_schedule_task
from bot.keyboards import days_of_week_options
from bot.functions import time_match, time_check, turn_to_time_type, send_days_of_week

schedule_router_add_task = Router()


class TaskWaiting(StatesGroup):
    days = State()
    time = State()
    task = State()


@schedule_router_add_task.message(Command('add_task'))
async def add_task(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(TaskWaiting.days)
    await state.update_data(days=[])
    await message.answer(f'Выберите дни, в которые будет выполняться задача. По окончании '
                         f'нажмите на клавишу "конец"', reply_markup=days_of_week_options)


@schedule_router_add_task.callback_query(F.data == 'mon')
async def add_mon(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Monday not in data.get('days'):
        data.get('days').append(DayOfWeek.Monday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'tue')
async def add_tue(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Tuesday not in data.get('days'):
        data.get('days').append(DayOfWeek.Tuesday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'wed')
async def add_wed(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Wednesday not in data.get('days'):
        data.get('days').append(DayOfWeek.Wednesday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'thu')
async def add_thu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Thursday not in data.get('days'):
        data.get('days').append(DayOfWeek.Thursday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'fri')
async def add_fri(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Friday not in data.get('days'):
        data.get('days').append(DayOfWeek.Friday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'sat')
async def add_sat(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Saturday not in data.get('days'):
        data.get('days').append(DayOfWeek.Saturday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'sun')
async def add_sun(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if DayOfWeek.Sunday not in data.get('days'):
        data.get('days').append(DayOfWeek.Sunday)
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'daily')
async def add_sun(callback: CallbackQuery, state: FSMContext):
    data: dict = {'days': [DayOfWeek.Monday,
                           DayOfWeek.Tuesday,
                           DayOfWeek.Wednesday,
                           DayOfWeek.Thursday,
                           DayOfWeek.Friday,
                           DayOfWeek.Saturday,
                           DayOfWeek.Sunday]}
    await state.update_data(days=data.get('days'))
    days = send_days_of_week(data.get('days'))
    await callback.message.answer(f'Выбранные дни: {days}')


@schedule_router_add_task.callback_query(F.data == 'end')
async def add_time(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(TaskWaiting.time)
    await callback.message.answer(f'Напишите время, в которое будет выполняться задача, в формате '
                                  f'час:мин - час:мин (12:30-13:30)')


@schedule_router_add_task.message(TaskWaiting.time)
async def add_text(message: Message, state: FSMContext):
    if not time_match(message.text) or not time_check(message.text):
        await message.answer('Неправильная запись, повторите попытку')
        return
    await state.update_data(time=message.text)
    await state.set_state(TaskWaiting.task)
    await message.answer('Напишите, что необходимо выполнить')


@schedule_router_add_task.message(TaskWaiting.task)
async def finish_adding_task(message: Message, state: FSMContext):
    if len(message.text) > 255:
        await message.answer('Описание не должно превышать 255 символов, повторите попытку')
        return
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    time_list = turn_to_time_type(data.get('time'))
    create_schedule_task(message.from_user.id, data.get('days'),
                         time_list[0], time_list[1], data.get('text'))
    days = send_days_of_week(data.get('days'))
    await message.answer(f'Задача добавлена!\n\n'
                         f'Дни недели: {days}\n'
                         f'Время: {data.get("time")}\n'
                         f'Задача: {data.get("text")}')
