import os

from aiogram import types

from data_b.dp_control import problem_translate_name
from handlers.math.problems_category_math import callback_problems, callback_problems_info


def get_inline_logic_problems_category():
    buttons = []

    all_category_names =

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
                                                      callback_data=callback_problems_info.new(info='Solution 1',
                                                                                               translate='Решение 1')))
        elif 'Решение 2' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                      callback_data=callback_problems_info.new(info='Solution 2',
                                                                                               translate='Решение 2')))
        elif 'Решение' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Решение', callback_data=callback_problems_info.new(info='Decision',
                                                                                                    translate='Решение')))
        elif 'Ответ' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Ответ',
                                           callback_data=callback_problems_info.new(info='Answer', translate='Ответ')))
        elif 'Подсказка' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Подсказка', callback_data=callback_problems_info.new(info='Hint',
                                                                                                      translate='Подсказка')))
        elif 'Замечания' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Замечания', callback_data=callback_problems_info.new(info='Remarks',
                                                                                                      translate='Замечания')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
