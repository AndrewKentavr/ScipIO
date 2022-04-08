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


def choose_category():
    buttons = [
        'Математика',
        'Логика'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


def admin_start_menu():
    buttons = [
        'Отправка сообщения всем',
        'Статистика пользователей',
        'Удалить задачу'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard