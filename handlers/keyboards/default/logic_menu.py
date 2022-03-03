from aiogram import types
from aiogram.utils import emoji


def get_keyboard_logic_start():
    buttons = [
        emoji.emojize(":book:") + ' Задания из категорий',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_logic_category():
    buttons = [
        emoji.emojize(":arrow_right:") + ' Следующая задача',
        emoji.emojize(":stop_sign:") + ' Закончить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
