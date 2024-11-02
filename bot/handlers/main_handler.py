from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'бот для дз и расписания\n'
                         f'/help')


@router.message(Command('help'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'/add_homework - добавить ДЗ\n'
                         f'/show_homework - посмотреть ДЗ\n'
                         f'/delete_homework - удалить ДЗ\n')