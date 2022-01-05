from aiogram import types


def get_keyboard_logic_start():
    buttons = [
        'Задания по категориям Логики',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_logic_answer():
    buttons = [
        'Посмотреть ответ',
        'Ответить 222'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
