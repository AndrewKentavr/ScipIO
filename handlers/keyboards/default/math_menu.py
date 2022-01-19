from aiogram import types
from aiogram.utils import emoji


def get_keyboard_math_start():
    buttons_1 = [
        emoji.emojize(":book:") + ' Задания из категорий Математики',
    ]
    buttons_2 = emoji.emojize(":brain:") + ' Примеры для подсчёта в уме'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons_1)
    keyboard.add(buttons_2)
    return keyboard


def get_keyboard_math_formulas():
    buttons = [
        'Продолжаем',
        'Закончить повторение'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_mentally_start():
    buttons = [
        'Да',
        'Отмена'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_mentally_end():
    buttons = [
        'Закончить примеры в уме'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_category():
    buttons = [
        emoji.emojize(":arrow_right:") + ' Следующая задача',
        emoji.emojize(":stop_sign:") + ' Закончить математику'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
