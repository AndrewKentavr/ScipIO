from aiogram import types
from aiogram.utils import emoji


def get_keyboard_flashcard_training_game():
    buttons = [
        emoji.emojize(":white_check_mark:") + ' Правильно',
        emoji.emojize(":x:") + ' Неправильно',
        'Обратная сторона',
        'Закончить тренировку'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_training_start():
    buttons = [
        'Да',
        'Нет',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_start():
    buttons = [
        emoji.emojize(":brain:") + ' Начать учить карточки',
        emoji.emojize(":gear:") + ' Управление карточками',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_flashcard_managing():
    buttons = [
        emoji.emojize(":pencil2:") + ' Создать карточку',
        emoji.emojize(":stop_sign:") + ' Удалить карточку',
        emoji.emojize(":information_source:") + ' Информация о карточках',
        'Показ карточек'
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


def setting_show():
    buttons = [
        'Фото',
        'Текст',
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
