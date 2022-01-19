from aiogram import types


def get_keyboard_logic_start():
    buttons = [
        'Задания из категорий Логики',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_logic_category():
    buttons = [
        'Следующая задача логика',
        'Закончить логику'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
