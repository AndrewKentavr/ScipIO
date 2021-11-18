from aiogram import types

from data_b.dp_control import finding_categories_table
from handlers.logic.tasks_category_logic import callback_problems_logic, callback_problems_info_logic


def get_inline_logic_problems_category():
    buttons = []

    list_all_categorys = finding_categories_table('logic')

    for i in list_all_categorys:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(
            types.InlineKeyboardButton(text=translated_name,
                                       callback_data=callback_problems_logic.new(category=category_name)))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_logic_problems_category_info(info_problem):
    buttons = []
    for i in info_problem:
        if i is None:
            continue

        elif 'Решение 1' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 1',
                                                      callback_data=callback_problems_info_logic.new(info='Solution 1',
                                                                                                     translate='Решение 1')))
        elif 'Решение 2' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                      callback_data=callback_problems_info_logic.new(info='Solution 2',
                                                                                                     translate='Решение 2')))
        elif 'Решение' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Решение',
                                           callback_data=callback_problems_info_logic.new(info='Decision',
                                                                                          translate='Решение')))
        elif 'Ответ' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Ответ',
                                           callback_data=callback_problems_info_logic.new(info='Answer',
                                                                                          translate='Ответ')))
        elif 'Подсказка' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Подсказка', callback_data=callback_problems_info_logic.new(info='Hint',
                                                                                                            translate='Подсказка')))
        elif 'Замечания' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Замечания',
                                           callback_data=callback_problems_info_logic.new(info='Remarks',
                                                                                          translate='Замечания')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
