from aiogram import types

from data_b.dp_control import finding_categories_table
from handlers.logic.tasks_category_logic import callback_problems_logic, callback_problems_info_logic


def get_inline_logic_problems_category():
    buttons = []

    # Список всех категории 'Logic'
    list_all_categorys = finding_categories_table('logic')

    for i in list_all_categorys:
        # НАПРИМЕР --- "riddles"
        category_name = i[0]
        # НАПРИМЕР --- "Загадки"
        translated_name = i[1]
        buttons.append(
            types.InlineKeyboardButton(text=translated_name,
                                       callback_data=callback_problems_logic.new(category_logic=category_name)))
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
                                                      callback_data=callback_problems_info_logic.new(
                                                          info_logic='Solution 1',
                                                          translate_logic='Решение 1')))
        elif 'Решение 2' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                      callback_data=callback_problems_info_logic.new(
                                                          info_logic='Solution 2',
                                                          translate_logic='Решение 2')))
        elif 'Решение' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Решение',
                                           callback_data=callback_problems_info_logic.new(info_logic='Decision',
                                                                                          translate_logic='Решение')))
        elif 'Ответ' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Ответ',
                                           callback_data=callback_problems_info_logic.new(info_logic='Answer',
                                                                                          translate_logic='Ответ')))
        elif 'Подсказка' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Подсказка',
                                           callback_data=callback_problems_info_logic.new(info_logic='Hint',
                                                                                          translate_logic='Подсказка')))
        elif 'Замечания' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Замечания',
                                           callback_data=callback_problems_info_logic.new(info_logic='Remarks',
                                                                                          translate_logic='Замечания')))
    buttons.append(
        types.InlineKeyboardButton(text='Следующее задание',
                                   callback_data=callback_problems_info_logic.new(info_logic='Next',
                                                                                  translate_logic='Следующее задание')))
    buttons.append(
        types.InlineKeyboardButton(text='Закончить',
                                   callback_data=callback_problems_info_logic.new(info_logic='Finish',
                                                                                  translate_logic='Закончить')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
