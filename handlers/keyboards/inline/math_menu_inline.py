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
    Создание inline-кнопок по всей информации, которая есть
    :param info_problem: Пример:
    ['Решение: Заметим сначала, что на автомате нельзя набрать чётное число. Следовательно, уПети не получится набрать число1982.Лемма. После первого умножения на3 невыгодно прибавлять4 более двух раз подряд.Доказательство леммы.  Заменив последовательность действий ×3, + 4, + 4, + 4 на +4, ×3, мы уменьшим затраты.Теперь можно восстановить последовательность действий Пети, начиная споследнего: если число не делится на3, то оно было получено прибавлениемчетвёрки, а если делится, то либо оно было получено умножением на3, либо при его получении были использованы только прибавления четвёрки. Таким образомполучаем, что оптимальная для Пети последовательность действий имеет вид:+4, + 4, + 4, + 4, + 4, ×3, + 4, + 4, ×3, + 4, ×3, + 4, + 4, ×3, + 4.', '', '', '']
    """
    print(info_problem)
    buttons = []
    for i in info_problem:
        if i is None:
            continue

        elif 'Решение 1' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 1',
                                                      callback_data=callback_problems_info_math.new(info='Solution 1',
                                                                                                    translate='Решение 1')))
        elif 'Решение 2' in i:
            buttons.append(types.InlineKeyboardButton(text='Решение 2',
                                                      callback_data=callback_problems_info_math.new(info='Solution 2',
                                                                                                    translate='Решение 2')))
        elif 'Решение' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Решение',
                                           callback_data=callback_problems_info_math.new(info='Decision',
                                                                                         translate='Решение')))
        elif 'Ответ' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Ответ',
                                           callback_data=callback_problems_info_math.new(info='Answer',
                                                                                         translate='Ответ')))
        elif 'Подсказка' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Подсказка', callback_data=callback_problems_info_math.new(info='Hint',
                                                                                                           translate='Подсказка')))
        elif 'Замечания' in i:
            buttons.append(
                types.InlineKeyboardButton(text='Замечания',
                                           callback_data=callback_problems_info_math.new(info='Remarks',
                                                                                         translate='Замечания')))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
