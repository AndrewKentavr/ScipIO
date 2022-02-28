from aiogram import types

from data_b.dp_control import finding_categories_table
from handlers.math.tasks_category_math import callback_problems_math, callback_problems_info_math


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
    """
    НУЖНО НАПИСАТЬ ЕЩЁ

    :return: Создаёт ко всем категориям Logic - INLINE кнопки
    """
    buttons = []

    # Находит все категории, которые есть в таблице math
    list_all_categorys = finding_categories_table('math')

    for i in list_all_categorys:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(
            types.InlineKeyboardButton(text=translated_name,
                                       callback_data=callback_problems_math.new(category=category_name)))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_math_problems_category_info(info_problem):
    """
    columns = 'decisions_1', 'decisions_2', 'answer', 'remarks'

    :param info_problem: Принимает значения columns
    :return: Возвращает INLINE - кнопки columns
    """

    buttons = []

    if info_problem['decisions_1'] != '':
        buttons.append(types.InlineKeyboardButton(text='Решение 1',
                                                  callback_data=callback_problems_info_math.new(
                                                      info='Decision 1',
                                                      translate='Решение 1')))

    if info_problem['decisions_2'] != '':
        buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                  callback_data=callback_problems_info_math.new(
                                                      info='Decision 2',
                                                      translate='Решение 2')))

    if info_problem['answer'] != '':
        buttons.append(types.InlineKeyboardButton(text='Ответ',
                                                  callback_data=callback_problems_info_math.new(
                                                      info='Answer',
                                                      translate='Ответ')))

    if info_problem['remarks'] != '':
        buttons.append(types.InlineKeyboardButton(text='Замечания',
                                                  callback_data=callback_problems_info_math.new(
                                                      info='Remarks',
                                                      translate='Замечания')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
