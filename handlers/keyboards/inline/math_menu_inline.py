import os

from aiogram import types

from data_b.dp_math import problem_translate_name
from handlers.math.problems_category_math import callback_problems, callback_problems_info


def get_inline_math_url():
    buttons = [
        types.InlineKeyboardButton(text="Хабр", url="https://habr.com/ru/post/207034/"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_inline_math_formulas():
    buttons = [
        types.InlineKeyboardButton(text="Вывести подсказку", callback_data="hint_f"),
        types.InlineKeyboardButton(text="Вывести ответ", callback_data="answer_f")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_math_problems_category():
    buttons = []

    all_files_names = os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json")

    for file_name_json in all_files_names:
        file_name = file_name_json.split('.json')[0]
        translated_name = problem_translate_name(file_name)
        buttons.append(
            types.InlineKeyboardButton(text=translated_name, callback_data=callback_problems.new(category=file_name)))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_math_problems_category_info(info_problem):
    buttons = []
    for i in info_problem:
        if 'Решение 1' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 1',
                                                      callback_data=callback_problems_info.new(info='Solution 1')))
        elif 'Решение 2' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                      callback_data=callback_problems_info.new(info='Solution 2')))
        elif 'Решение' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Решение', callback_data=callback_problems_info.new(info='Decision')))
        elif 'Ответ' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Ответ', callback_data=callback_problems_info.new(info='Answer')))
        elif 'Подсказка' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Подсказка', callback_data=callback_problems_info.new(info='Hint')))
        elif 'Замечания' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Замечания', callback_data=callback_problems_info.new(info='Remarks')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
