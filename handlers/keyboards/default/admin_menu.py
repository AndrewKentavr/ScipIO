from aiogram import types


def choose_send():
    buttons = [
        'Да',
        'Отмена'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def add_text():
    buttons = [
        'Добавить',
        'Нет, хочу отправить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def main_send_msg():
    buttons = [
        'Отправка сообщения всем',
        'Статистика пользователей'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard