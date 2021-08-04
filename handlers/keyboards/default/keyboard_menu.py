from aiogram import types


def get_keyboard_math_start():
    buttons = [
        'Задачки',
        'Примеры для подчёта в уме',
        'Поставить таймер на отправку заданий'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
