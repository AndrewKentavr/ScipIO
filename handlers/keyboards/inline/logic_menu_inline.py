from aiogram import types

from data_b.dp_control import finding_categories_table
from handlers.math.problems_category_math import callback_problems, callback_problems_info


def get_inline_logic_problems_category():
    buttons = []

    list_all_categorys = finding_categories_table('logic')

    for i in list_all_categorys:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(
            types.InlineKeyboardButton(text=translated_name, callback_data=callback_problems.new(category=category_name)))
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
