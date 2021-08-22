from aiogram import types


def get_keyboard_logic_start():
    buttons = [
        'Данетки',
        'Загадки',
        'Задачки собеседований'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
