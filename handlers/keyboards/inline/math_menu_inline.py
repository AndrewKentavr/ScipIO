from aiogram import types


def get_inline_math_url():
    buttons = [
        types.InlineKeyboardButton(text="Хабр", url="https://habr.com/ru/post/207034/"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_inline_math_formulas():
    buttons = [
        types.InlineKeyboardButton(text="Вывести подсказку", callback_data="151515"),
        types.InlineKeyboardButton(text="Вывести ответ", callback_data="1616161")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard
