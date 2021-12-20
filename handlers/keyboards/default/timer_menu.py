from aiogram import types


def get_keyboard_timer():
    buttons = [
        'Создать таймер',
        'Удалить таймер',
        'Посмотреть все таймеры'
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
