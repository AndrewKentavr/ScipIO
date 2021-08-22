from aiogram import types


def get_keyboard_math_start():
    buttons_1 = [
        'Задания по категориям',
        'Формулы',
    ]
    buttons_2 = 'Примеры для подсчёта в уме'
    buttons_3 = 'Математический таймер'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons_1)
    keyboard.add(buttons_2)
    keyboard.add(buttons_3)
    return keyboard


def get_keyboard_math_end():
    buttons = [
        'Продолжаем, я деньги за это заплатил',
        'Закончить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_end_problem():
    buttons = [
        'Продолжаем, я деньги за это заплатил',
        'Закончить задачки'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_timer():
    buttons = [
        'Создать таймер',
        'Удалить таймер',
        'Посмотреть все таймеры'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_formulas():
    buttons = [
        'Продолжаем',
        'Закончить повторение'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard