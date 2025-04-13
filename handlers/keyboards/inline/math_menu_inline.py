from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.dp_control import finding_categories_table, finding_one_categories_table
from database.dp_control import finding_main_categories_table
from database import dp_control
from handlers.problems.tasks_category_math import callback_main_problems_math, callback_problems_info_math, \
    callback_problems_math


def get_inline_math_url():
    buttons = [
        InlineKeyboardButton(text="Хабр", url="https://habr.com/ru/post/207034/"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_inline_math_formulas():
    buttons = [
        InlineKeyboardButton(text="Вывести подсказку", callback_data="hint_f"),
        InlineKeyboardButton(text="Вывести ответ", callback_data="answer_f")
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_math_categories(category):
    categories = dp_control.get_math_categories(category)
    buttons = []
    for i in categories:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(
            InlineKeyboardButton(text=translated_name,
                                 callback_data=callback_main_problems_math.new(category=category_name)))

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_inline_math_problems_category():
    """
    НУЖНО НАПИСАТЬ ЕЩЁ

    :return: Создаёт ко всем категориям Logic - INLINE кнопки
    """
    buttons = []

    # Находит все категории, которые есть в таблице problems
    list_all_categories = finding_categories_table('problems')

    for i in list_all_categories:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(
            InlineKeyboardButton(text=translated_name,
                                 callback_data=callback_main_problems_math.new(category=category_name)))
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_main_math_problems_category():
    """
    НУЖНО НАПИСАТЬ ЕЩЁ

    :return: Создаёт ко всем категориям Logic - INLINE кнопки
    """
    buttons = []

    # Находит все категории, которые есть в таблице problems
    list_all_categories = sorted(finding_main_categories_table('problems'))
    for i in list_all_categories:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(InlineKeyboardButton(text=translated_name, callback_data=callback_main_problems_math.new(
            category=category_name)))
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_one_main_math_problems_category(category):
    list_all_categories = sorted(finding_one_categories_table(category))
    buttons = []
    for i in list_all_categories:
        category_name = i[0]  # НАПРИМЕР --- "riddles"
        translated_name = i[1]  # НАПРИМЕР --- "Загадки"
        buttons.append(InlineKeyboardButton(text=translated_name,
                                            callback_data=callback_problems_math.new(category=category_name)))
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_math_problems_category_info(info_problem):
    """
    columns = 'decisions_1', 'decisions_2', 'answer', 'remarks'

    :param info_problem: Принимает значения columns
    :return: Возвращает INLINE - кнопки columns
    """

    buttons = []

    if info_problem['decisions_1'] != '' and info_problem['decisions_1'] is not None:
        buttons.append(InlineKeyboardButton(text='Решение 1',
                                            callback_data=callback_problems_info_math.new(
                                                info='decisions_1')))

    if info_problem['decisions_2'] != '' and info_problem['decisions_2'] is not None:
        buttons.append(InlineKeyboardButton(text='Решение 2',
                                            callback_data=callback_problems_info_math.new(
                                                info='decisions_2')))

    if info_problem['answer'] != '' and info_problem['answer'] is not None:
        buttons.append(InlineKeyboardButton(text='Ответ',
                                            callback_data=callback_problems_info_math.new(
                                                info='answer')))

    if info_problem['remarks'] != '' and info_problem['remarks'] is not None:
        buttons.append(InlineKeyboardButton(text='Замечания',
                                            callback_data=callback_problems_info_math.new(
                                                info='remarks')))

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
