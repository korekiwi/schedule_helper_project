from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from databases.db import (get_all_subjects, delete_all_finished_tasks,
                          delete_all_finished_tasks_by_subject, hard_delete, check_task_id,
                          delete_task_by_id)
from bot.keyboards import hard_delete_options, delete_options

homework_router_delete = Router()


class DeleteWaiting(StatesGroup):
    subject = State()


class DeleteIDWaiting(StatesGroup):
    id = State()


@homework_router_delete.message(Command('delete_homework'))
async def remove_homework(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Удалить:', reply_markup=delete_options)


@homework_router_delete.callback_query(F.data == 'del_hom1')
async def remove_all_finished_tasks(callback: CallbackQuery):
    delete_all_finished_tasks(callback.from_user.id)
    await callback.message.answer('Все выполненные задания удалены')


@homework_router_delete.callback_query(F.data == 'del_hom2')
async def get_subject_to_remove_all_finished_tasks(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteWaiting.subject)
    await callback.message.answer('Напишите название предмета, по которому необходимо удалить все '
                                  'выполненные задания')


@homework_router_delete.message(DeleteWaiting.subject)
async def remove_all_finished_tasks(message: Message, state: FSMContext):
    if message.text.capitalize() not in get_all_subjects(message.from_user.id):
        await message.answer(f'Нет заданий по предмету {message.text.capitalize()}')
        return
    await state.update_data(subject=message.text.capitalize())
    data = await state.get_data()
    await state.clear()
    delete_all_finished_tasks_by_subject(message.from_user.id, data.get('subject'))
    await message.answer(f"Все выполненные задания по предмету {data.get('subject')} удалены")


@homework_router_delete.callback_query(F.data == 'del_hom3')
async def get_id_to_remove_task_by_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteIDWaiting.id)
    await callback.message.answer('Напишите ID задания, которое хотите удалить')


@homework_router_delete.message(DeleteIDWaiting.id)
async def remove_task_by_id(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задания с таким ID, повторите попытку')
        return
    await state.update_data(id=message.text)
    data = await state.get_data()
    await state.clear()
    delete_task_by_id(message.from_user.id, data.get('id'))
    await message.answer('Задание удалено')


@homework_router_delete.callback_query(F.data == 'del_hom4')
async def remove_all_tasks(callback: CallbackQuery):
    await callback.message.answer(f'Вы уверены, что хотите удалить все задания? '
                                  f'Данное действие необратимо.', reply_markup=hard_delete_options)


@homework_router_delete.callback_query(F.data == 'hard_del1')
async def hard_delete_activated(callback: CallbackQuery):
    hard_delete(callback.from_user.id)
    await callback.message.answer('Все задания удалены')


@homework_router_delete.callback_query(F.data == 'hard_del2')
async def hard_delete_unactivated(callback: CallbackQuery):
    await callback.message.answer('Экстремальная чистка отменена')
