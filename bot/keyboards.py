from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
