from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.functions import send_all_homework
from databases.db import get_all_subjects, get_homework_by_subject
from bot.keyboards import view_options


homework_router_show = Router()


class ShowHomework(StatesGroup):
    subject = State()


@homework_router_show.message(Command('show_homework'))
async def show_homework(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Посмотреть:', reply_markup=view_options)


@homework_router_show.callback_query(F.data == 'hom1')
async def show_all_subjects(callback: CallbackQuery):
    subjects = get_all_subjects(callback.from_user.id)
    text_message = 'Предметы: \n'
    for subject in subjects:
        text_message += subject + '\n'
    await callback.message.answer(text_message)


@homework_router_show.callback_query(F.data == 'hom2')
async def get_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ShowHomework.subject)
    await callback.message.answer('Напишите название предмета')


@homework_router_show.message(ShowHomework.subject)
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
