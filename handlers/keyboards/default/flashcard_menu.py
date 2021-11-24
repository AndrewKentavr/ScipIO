from aiogram import types


def get_keyboard_flashcard_start():
    buttons = [
        'Создать карточку',
        'Удалить карточку',
        'Информация о карточках'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
