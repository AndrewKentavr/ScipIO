"""
Какая - то тут жопа с CallbackData, а конкретнее нужно посмотреть что за translate

ТАКЖЕ СДЕЛАНА НЕ ОЧЕНЬ КНОПКА "СЛЕДУЮЩЕЕ ЗАДАНИЕ"
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from data_b.dp_control import problem_category_random, finding_categories_table
from handlers.keyboards.default import logic_menu

callback_problems_logic = CallbackData("problems_logic", "category_logic")
callback_problems_info_logic = CallbackData("values_logic", "info_logic", "translate_logic")


async def tasks_category_logic_start(message: types.Message):
    from handlers.keyboards.inline import logic_menu_inline

    await message.answer('Выберете категорию заданий:',
                         reply_markup=logic_menu_inline.get_inline_logic_problems_category())


async def tasks_category_logic_print_keyboard_inline(call: types.CallbackQuery, callback_data: dict):
    # НУЖНЫ ИЗМЕНЕНИЯ В КОММЕНТАРИИ

    """

    :param call: Это ответ на нажатие INLINE кнопки КАТЕГОРИЯ
    :param callback_data: Это значения INLINE кнопки, то есть это информация
    о категории (её вроде бы info_logic, translate_logic)
    :return:
    """
    from handlers.keyboards.inline import logic_menu_inline

    # объявлен global, чтобы при нажатии "Следующее задание" выводило туже категорию
    global category
    category = callback_data["category_logic"]
    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    dictionary_info_problem = problem_category_random(category, 'logic')

    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])

    global problems_info_data_logic
    problems_info_data_logic = info_problem

    await call.message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
        reply_markup=logic_menu.get_keyboard_logic_category())
    await call.message.answer(f'{condition}',
                              reply_markup=logic_menu_inline.get_inline_logic_problems_category_info(info_problem))

    await call.answer()


async def tasks_category_logic_print_keyboard_default(message: types.Message):
    from handlers.keyboards.inline import logic_menu_inline

    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    dictionary_info_problem = problem_category_random(category, 'logic')

    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])
    
    await message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
        reply_markup=logic_menu.get_keyboard_logic_category())
    await message.answer(f'{condition}',
                         reply_markup=logic_menu_inline.get_inline_logic_problems_category_info(info_problem))


async def tasks_category_logic_print_info(call: types.CallbackQuery, callback_data: dict):
    """
    ВОТ ТУТ НУЖНО ИСПРАВЛЯТЬ, Т.К ТУТ НЕПОНЯТНО ЗАЧЕМ НУЖЕН TRANSLATE, ЕСЛИ ЕСТЬ info_logic
    """

    translate = callback_data['translate_logic']

    if translate == 'Решение 1':
        await call.message.answer(f'{problems_info_data_logic["decisions_1"]}')
    elif translate == 'Решение 2':
        await call.message.answer(f'{problems_info_data_logic["decisions_2"]}')
    elif translate == 'Ответ':
        await call.message.answer(f'{problems_info_data_logic["answer"]}')
    elif translate == 'Замечания':
        await call.message.answer(f'{problems_info_data_logic["remarks"]}')

    await call.answer()


def register_handlers_tasks_logic_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_logic_start, Text(equals="Задания по категориям Логики"))

    all_files_names = [i[0] for i in finding_categories_table('logic')]
    dp.register_callback_query_handler(tasks_category_logic_print_keyboard_inline,
                                       callback_problems_logic.filter(category_logic=all_files_names), state='*')

    dp.register_message_handler(tasks_category_logic_print_keyboard_default, Text(equals="Следующая задача"))

    info = ['Decision 1', 'Decision 2', 'Answer', 'Remarks']
    dp.register_callback_query_handler(tasks_category_logic_print_info,
                                       callback_problems_info_logic.filter(info_logic=info), state='*')
