from aiogram import types


def get_keyboard_math_start():
    buttons_1 = [
        'Задания по категориям Математики',
    ]
    buttons_2 = 'Примеры для подсчёта в уме'
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
        'Закончить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
