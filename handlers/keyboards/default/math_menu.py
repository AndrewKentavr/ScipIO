from aiogram import types
from aiogram.utils import emoji

from database import dp_control


def get_keyboard_math_start(message: types.Message):
    buttons_1 = [
        emoji.emojize(":book:") + ' Задания из категорий',
        emoji.emojize(":brain:") + ' Примеры для подсчёта в уме'
    ]
    value = dp_control.show_img_check(message.from_user.id)
    if value == 1:
        buttons_1.append(emoji.emojize(":gear:") + ' Выключить задачи с фотографиями')
    elif value == 0:
        buttons_1.append(emoji.emojize(":gear:") + ' Включить задачи с фотографиями')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    keyboard.add(*buttons_1)
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
        emoji.emojize(":stop_sign:") + " Закончить",
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_math_category():
    buttons = [
        emoji.emojize(":white_check_mark:") + ' Правильно',
        emoji.emojize(":x:") + ' Неправильно',
        emoji.emojize(":stop_sign:") + ' Закончить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
