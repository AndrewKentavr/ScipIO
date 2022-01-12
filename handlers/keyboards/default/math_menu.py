from aiogram import types


def get_keyboard_math_start():
    buttons_1 = [
        'Задания по категориям Математики',
        'Формулы',
    ]
    buttons_2 = 'Примеры для подсчёта в уме'
    buttons_3 = 'Математический таймер'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons_1)
    keyboard.add(buttons_2)
    keyboard.add(buttons_3)
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
