from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_keyboard

router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'бот для дз и расписания\n'
                         f'/help', reply_markup=main_keyboard)


@router.message(Command('clear'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено')


@router.message(Command('help'))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'ДЗ:\n'
                         f'/add_homework - добавить ДЗ\n'
                         f'/show_homework - посмотреть ДЗ\n'
                         f'/delete_homework - удалить ДЗ\n'
                         f'/mark_completed - отметить ДЗ выполненным\n'
                         f'/hw_notifications - настроить уведомления'
                         f'\n\n'
                         f'Расписание:\n'
                         f'/add_task - добавить задачу\n'
                         f'/show_tasks - посмотреть задачи\n'
                         f'/delete_tasks - удалить задачи\n'
                         f'/sched_notifications - настроить уведомления')
