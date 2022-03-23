from aiogram import Bot, Dispatcher, executor, types


def choose_send():
    buttons = [
        'Да',
        'Нет'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def add_text():
    buttons = [
        'Добавить',
        'Нет, хочу отправить'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def main_send_msg():
    buttons = [
        'Отправка сообщения всем'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
