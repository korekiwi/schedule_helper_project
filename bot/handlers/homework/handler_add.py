from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.functions import date_match, turn_to_date_type
from databases.db import create_homework

homework_router_add = Router()


class HomeworkWaiting(StatesGroup):
    user_id = State()
    subject = State()
    date = State()
    text = State()


@homework_router_add.message(Command('add_homework'))
async def add_homework(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(HomeworkWaiting.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(HomeworkWaiting.subject)
    await message.answer('Напишите название предмета.')


@homework_router_add.message(HomeworkWaiting.subject)
async def fill_subject(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer('Название слишком длинное, повторите попытку')
        return
    await state.update_data(subject=message.text.capitalize())
    await state.set_state(HomeworkWaiting.date)
    await message.answer('Напишите срок выполнения работы в формате год-месяц-число')


@homework_router_add.message(HomeworkWaiting.date)
async def fill_date(message: Message, state: FSMContext):
    if not date_match(message.text):
        await message.answer('Неправильная запись, повторите попытку')
        return
    await state.update_data(date=message.text)
    await state.set_state(HomeworkWaiting.text)
    await message.answer('Напишите, что необходимо выполнить')


@homework_router_add.message(HomeworkWaiting.text)
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
