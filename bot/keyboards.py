from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/help')],
    [KeyboardButton(text='/clear')],
], resize_keyboard=True)

hw_notifications_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Включить', callback_data='hw_turn_on')],
    [InlineKeyboardButton(text='Выключить', callback_data='hw_turn_off')],
    ])

sched_notifications_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Включить', callback_data='sched_turn_on')],
    [InlineKeyboardButton(text='Выключить', callback_data='sched_turn_off')],
    ])

delete_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Все выполненные задания', callback_data='del_hom1')],
    [InlineKeyboardButton(text='Все выполненные задания по кокретному предмету', callback_data='del_hom2')],
    [InlineKeyboardButton(text='По ID задания', callback_data='del_hom3')],
    [InlineKeyboardButton(text='Все задания (экстремальная чистка)', callback_data='del_hom4')]
    ])

view_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои предметы', callback_data='hom1')],
    [InlineKeyboardButton(text='Задания по конкретному предмету', callback_data='hom2')]
])

hard_delete_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='hard_del1')],
    [InlineKeyboardButton(text='Нет', callback_data='hard_del2')]
])

days_of_week_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Понедельник', callback_data='mon')],
    [InlineKeyboardButton(text='Вторник', callback_data='tue')],
    [InlineKeyboardButton(text='Среда', callback_data='wed')],
    [InlineKeyboardButton(text='Четверг', callback_data='thu')],
    [InlineKeyboardButton(text='Пятница', callback_data='fri')],
    [InlineKeyboardButton(text='Суббота', callback_data='sat')],
    [InlineKeyboardButton(text='Воскресенье', callback_data='sun')],
    [InlineKeyboardButton(text='Ежедневно', callback_data='daily')],
    [InlineKeyboardButton(text='Конец', callback_data='end')],
])

days_of_week_view_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сегодня', callback_data='today')],
    [InlineKeyboardButton(text='Понедельник', callback_data='mon_view')],
    [InlineKeyboardButton(text='Вторник', callback_data='tue_view')],
    [InlineKeyboardButton(text='Среда', callback_data='wed_view')],
    [InlineKeyboardButton(text='Четверг', callback_data='thu_view')],
    [InlineKeyboardButton(text='Пятница', callback_data='fri_view')],
    [InlineKeyboardButton(text='Суббота', callback_data='sat_view')],
    [InlineKeyboardButton(text='Воскресенье', callback_data='sun_view')],
])

schedule_delete_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Все задачи в конкретный день', callback_data='del_sched1')],
    [InlineKeyboardButton(text='По ID конкретную задачу', callback_data='del_sched2')],
    [InlineKeyboardButton(text='По ID одной задачи серию задач (с одинаковым описанием)', callback_data='del_sched3')],
    [InlineKeyboardButton(text='Все задачи (экстремальная чистка)', callback_data='del_sched4')]
    ])

days_of_week_delete_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Понедельник', callback_data='mon_del')],
    [InlineKeyboardButton(text='Вторник', callback_data='tue_del')],
    [InlineKeyboardButton(text='Среда', callback_data='wed_del')],
    [InlineKeyboardButton(text='Четверг', callback_data='thu_del')],
    [InlineKeyboardButton(text='Пятница', callback_data='fri_del')],
    [InlineKeyboardButton(text='Суббота', callback_data='sat_del')],
    [InlineKeyboardButton(text='Воскресенье', callback_data='sun_del')],
])

hard_delete_schedule_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='sched_hard_del1')],
    [InlineKeyboardButton(text='Нет', callback_data='sched_hard_del2')]
])