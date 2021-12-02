from aiogram import types


def get_keyboard_flashcard_training_start():
    buttons = [
        'Да',
        'Отмена',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_start():
    buttons = [
        'Начать учить карточки',
        'Управление карточками',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_managing():
    buttons = [
        'Создать карточку',
        'Удалить карточку',
        'Информация о карточках'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_end_que():
    buttons = [
        'Да',
        'Нет',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
