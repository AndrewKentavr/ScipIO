from aiogram import types
from aiogram.utils import emoji


def get_keyboard_statistics_start():
    buttons = [
        emoji.emojize(":bar_chart:") + ' Общая',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
