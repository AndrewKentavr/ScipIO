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
    """
    columns = 'decisions_1', 'decisions_2', 'answer', 'remarks'

    :param info_problem: Принимает значения columns
    :return: Возвращает INLINE - кнопки columns
    """

    buttons = []

    if info_problem['decisions_1'] != '':
        buttons.append(types.InlineKeyboardButton(text='Решение 1',
                                                  callback_data=callback_problems_info_logic.new(
                                                      info_logic='Decision 1',
                                                      translate_logic='Решение 1')))
    if info_problem['decisions_2'] != '':
        buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                  callback_data=callback_problems_info_logic.new(
                                                      info_logic='Decision 2',
                                                      translate_logic='Решение 2')))
    if info_problem['answer'] != '':
        buttons.append(
            types.InlineKeyboardButton(text='Ответ',
                                       callback_data=callback_problems_info_logic.new(info_logic='Answer',
                                                                                      translate_logic='Ответ')))
    if info_problem['remarks'] != '':
        buttons.append(
            types.InlineKeyboardButton(text='Замечания',
                                       callback_data=callback_problems_info_logic.new(info_logic='Remarks',
                                                                                      translate_logic='Замечания')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
