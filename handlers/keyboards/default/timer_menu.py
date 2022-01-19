from aiogram import types
from aiogram.utils import emoji


def get_keyboard_timer():
    buttons = [
        emoji.emojize(":pencil2:") + ' Создать таймер',
        emoji.emojize(":stop_sign:") + ' Удалить таймер',
        emoji.emojize(":information_source:") + ' Посмотреть ваши таймеры'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_question_tasks():
    buttons = [
        'Карточки (Flashcards)',
        'Математика в уме',
        'Задачи по математике',
        'Задачи по логике'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
