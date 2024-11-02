from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from databases.db import check_task_id, change_status

homework_router_mark = Router()


class MarkIDWaiting(StatesGroup):
    id = State()


@homework_router_mark.message(Command('mark_completed'))
async def get_id_to_mark_completed(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MarkIDWaiting.id)
    await message.answer('Напишите ID задания, которое нужно отметить выполненным')


@homework_router_mark.message(MarkIDWaiting.id)
async def mark_completed(message: Message, state: FSMContext):
    if not isinstance(message.text, int) and not check_task_id(message.from_user.id, message.text):
        await message.answer('Не существует задания с таким ID, повторите попытку')
        return
    await state.update_data(id=message.text)
    data = await state.get_data()
    await state.clear()
    change_status(message.from_user.id, data.get('id'), 1)
    await message.answer(f'Задание с ID {data.get("id")} отмечено выполненным')
