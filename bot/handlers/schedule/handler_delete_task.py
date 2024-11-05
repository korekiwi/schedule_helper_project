from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.keyboards import (schedule_delete_options, days_of_week_delete_options,
                           hard_delete_schedule_options)
from databases.models import DayOfWeek
from databases.db import (delete_schedule_tasks_by_day, check_schedule_task_id,
                          delete_schedule_task_by_id, delete_schedule_tasks_by_id,
                          schedule_hard_delete)

schedule_router_delete_task = Router()


class DeleteIDWaiting(StatesGroup):
    task_id = State()


class GroupDeleteIDWaiting(StatesGroup):
    task_id = State()


@schedule_router_delete_task.message(Command('delete_tasks'))
async def delete_task(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Удалить:', reply_markup=schedule_delete_options)


"""по дню недели"""


@schedule_router_delete_task.callback_query(F.data == 'del_sched1')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Выберите день, в которой нужно удалить все задачи:',
                                  reply_markup=days_of_week_delete_options)


@schedule_router_delete_task.callback_query(F.data == 'mon_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Monday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'tue_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Tuesday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'wed_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Wednesday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'thu_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Thursday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'fri_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Friday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'sat_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Saturday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'sun_del')
async def delete_by_day(callback: CallbackQuery, state: FSMContext):
    day = DayOfWeek.Sunday
    delete_schedule_tasks_by_day(callback.from_user.id, day)
    await callback.message.answer(f'{day.value.capitalize()}: все задачи удалены.')


"""по ID"""


@schedule_router_delete_task.callback_query(F.data == 'del_sched2')
async def delete_by_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteIDWaiting.task_id)
    await callback.message.answer(text='Напишите ID задачи, которую нужно удалить')


@schedule_router_delete_task.message(DeleteIDWaiting.task_id)
async def delete_by_id(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_schedule_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задачи с таким ID, повторите попытку')
        return
    await state.update_data(task_id=message.text)
    data = await state.get_data()
    await state.clear()
    delete_schedule_task_by_id(message.from_user.id, int(data.get('task_id')))
    await message.answer('Задача удалена.')


"""по ID серию задач"""


@schedule_router_delete_task.callback_query(F.data == 'del_sched3')
async def delete_group_by_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroupDeleteIDWaiting.task_id)
    await callback.message.answer(text='Напишите ID любой задачи из серии, которую нужно удалить')


@schedule_router_delete_task.message(GroupDeleteIDWaiting.task_id)
async def delete_group_by_id(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_schedule_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задачи с таким ID, повторите попытку')
        return
    await state.update_data(task_id=message.text)
    data = await state.get_data()
    await state.clear()
    delete_schedule_tasks_by_id(message.from_user.id, int(data.get('task_id')))
    await message.answer('Задачи удалены.')


"""все задачи"""


@schedule_router_delete_task.callback_query(F.data == 'del_sched4')
async def sched_hard_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Вы уверены, что хотите удалить все задания? '
                                  f'Данное действие необратимо.',
                                  reply_markup=hard_delete_schedule_options)


@schedule_router_delete_task.callback_query(F.data == 'sched_hard_del1')
async def sched_hard_delete(callback: CallbackQuery, state: FSMContext):
    schedule_hard_delete(callback.from_user.id)
    await callback.message.answer('Все задачи удалены.')


@schedule_router_delete_task.callback_query(F.data == 'sched_hard_del2')
async def sched_hard_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Экстремальная чистка отменена.')