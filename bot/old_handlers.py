from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.functions import date_match, turn_to_date_type, send_all_homework
from databases.db import (create_homework, get_all_subjects,
                          get_homework_by_subject, delete_all_finished_tasks,
                          delete_all_finished_tasks_by_subject,
                          check_task_id, hard_delete, delete_task_by_id,
                          change_status)
from databases.models import Homework
import keyboards as kb

router = Router()


class HomeworkWaiting(StatesGroup):
    user_id = State()
    subject = State()
    date = State()
    text = State()


class ShowHomework(StatesGroup):
    subject = State()


class DeleteWaiting(StatesGroup):
    subject = State()


class DeleteIDWaiting(StatesGroup):
    id = State()


class MarkIDWaiting(StatesGroup):
    id = State()


@router.message(Command('start'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'бот для дз и прочей хрени\n'
                         f'/help')


@router.message(Command('help'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'/add_homework - добавить ДЗ\n'
                         f'/show_homework - посмотреть ДЗ\n'
                         f'/delete_homework - удалить ДЗ\n')

"""Добавление ДЗ"""


@router.message(Command('add_homework'))
async def add_homework(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(HomeworkWaiting.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(HomeworkWaiting.subject)
    await message.answer('Напишите название предмета.')


@router.message(HomeworkWaiting.subject)
async def fill_subject(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer('Название слишком длинное, повторите попытку')
        return
    await state.update_data(subject=message.text.capitalize())
    await state.set_state(HomeworkWaiting.date)
    await message.answer('Напишите срок выполнения работы в формате год-месяц-число')


@router.message(HomeworkWaiting.date)
async def fill_date(message: Message, state: FSMContext):
    if not date_match(message.text):
        await message.answer('Неправильная запись, повторите попытку')
        return
    await state.update_data(date=message.text)
    await state.set_state(HomeworkWaiting.text)
    await message.answer('Напишите, что необходимо выполнить')


@router.message(HomeworkWaiting.text)
async def fill_date(message: Message, state: FSMContext):
    if len(message.text) > 1000:
        await message.answer('Описание не должно превышать 1000 символов, повторите попытку')
        return
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    create_homework(data.get('user_id'), data.get('subject'),
                    data.get('text'), turn_to_date_type(data.get('date')))
    await message.answer(f"Задание добавлено! \n\n"
                         f"Предмет: {data.get('subject')}\n"
                         f"Выполнить до: {data.get('date')}\n"
                         f"Задание: {data.get('text')}")
    print('кто-то добавился')


"""Просмотр ДЗ"""


@router.message(Command('show_homework'))
async def show_homework(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Посмотреть:', reply_markup=kb.view_options)


@router.callback_query(F.data == 'hom1')
async def show_all_subjects(callback: CallbackQuery):
    subjects = get_all_subjects(callback.from_user.id)
    text_message = 'Предметы: \n'
    for subject in subjects:
        text_message += subject + '\n'
    await callback.message.answer(text_message)


@router.callback_query(F.data == 'hom2')
async def get_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ShowHomework.subject)
    await callback.message.answer('Напишите название предмета')


@router.message(ShowHomework.subject)
async def show_homework(message: Message, state: FSMContext):
    if message.text.capitalize() not in get_all_subjects(message.from_user.id):
        await message.answer(f'Нет заданий по предмету {message.text.capitalize()}')
        return
    await state.update_data(subject=message.text.capitalize())
    data = await state.get_data()
    await state.clear()
    homework_list = get_homework_by_subject(message.from_user.id, data.get('subject'))
    message_text = send_all_homework(homework_list)
    await message.answer(message_text)


"""Удаление ДЗ"""


@router.message(Command('delete_homework'))
async def remove_homework(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Удалить:', reply_markup=kb.delete_options)


@router.callback_query(F.data == 'del_hom1')
async def remove_all_finished_tasks(callback: CallbackQuery):
    delete_all_finished_tasks(callback.from_user.id)
    await callback.message.answer('Все выполненные задания удалены')


@router.callback_query(F.data == 'del_hom2')
async def get_subject_to_remove_all_finished_tasks(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteWaiting.subject)
    await callback.message.answer('Напишите название предмета, по которому необходимо удалить все '
                                  'выполненные задания')


@router.message(DeleteWaiting.subject)
async def remove_all_finished_tasks(message: Message, state: FSMContext):
    if message.text.capitalize() not in get_all_subjects(message.from_user.id):
        await message.answer(f'Нет заданий по предмету {message.text.capitalize()}')
        return
    await state.update_data(subject=message.text.capitalize())
    data = await state.get_data()
    await state.clear()
    delete_all_finished_tasks_by_subject(message.from_user.id, data.get('subject'))
    await message.answer(f"Все выполненные задания по предмету {data.get('subject')} удалены")


@router.callback_query(F.data == 'del_hom3')
async def get_id_to_remove_task_by_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteIDWaiting.id)
    await callback.message.answer('Напишите ID задания, которое хотите удалить')


@router.message(DeleteIDWaiting.id)
async def remove_task_by_id(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задания с таким ID, повторите попытку')
        return
    await state.update_data(id=message.text)
    data = await state.get_data()
    await state.clear()
    delete_task_by_id(message.from_user.id, data.get('id'))
    await message.answer('Задание удалено')


@router.callback_query(F.data == 'del_hom4')
async def remove_all_tasks(callback: CallbackQuery):
    await callback.message.answer(f'Вы уверены, что хотите удалить все задания? '
                                  f'Данное действие необратимо.', reply_markup=kb.hard_delete_options)


@router.callback_query(F.data == 'hard_del1')
async def hard_delete_activated(callback: CallbackQuery):
    hard_delete(callback.from_user.id)
    await callback.message.answer('Все задания удалены')


@router.callback_query(F.data == 'hard_del2')
async def hard_delete_unactivated(callback: CallbackQuery):
    await callback.message.answer('Экстремальная чистка отменена')


"""Отметить выполненным"""


@router.message(Command('mark_completed'))
async def get_id_to_mark_completed(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MarkIDWaiting.id)
    await message.answer('Напишите ID задания, которое нужно отметить выполненным')


@router.message(MarkIDWaiting.id)
async def mark_completed(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задания с таким ID, повторите попытку')
        return
    await state.update_data(id=message.text)
    data = await state.get_data()
    await state.clear()
    change_status(message.from_user.id, data.get('id'), 1)
    await message.answer(f'Задание с ID {data.get("id")} отмечено выполненным')

