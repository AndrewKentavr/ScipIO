from aiogram import types


def get_keyboard_logic_start():
    buttons = [
        'Задания по категориям',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
