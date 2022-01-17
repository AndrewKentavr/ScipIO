from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from data_b.dp_control import problem_category_random, finding_categories_table

callback_problems_logic = CallbackData("problems_logic", "category_logic")
callback_problems_info_logic = CallbackData("values_logic", "info_logic", "translate_logic")


async def tasks_category_logic_start(message: types.Message):
    from handlers.keyboards.inline import logic_menu_inline

    await message.answer('Выберите категорию заданий:',
                         reply_markup=logic_menu_inline.get_inline_logic_problems_category())


async def tasks_category_logic_print(call: types.CallbackQuery, callback_data: dict):
    # НУЖНЫ ИЗМЕНЕНИЯ В КОММЕНТАРИИ

    """

    :param call: Это ответ на нажатие INLINE кнопки КАТЕГОРИЯ
    :param callback_data: Это значения INLINE кнопки, то есть это информация
    о категории (её вроде бы info_logic, translate_logic)
    :return:
    """
    from handlers.keyboards.inline import logic_menu_inline

    category = callback_data["category_logic"]
    list_info_problem = problem_category_random(category, 'logic')
    title = list_info_problem[0]
    href = list_info_problem[1]
    subcategory = list_info_problem[2]
    complexity, classes = list_info_problem[3], list_info_problem[4]
    condition = list_info_problem[5]
    info_problem = list_info_problem[6:]
    global problems_info_data_logic
    problems_info_data_logic = info_problem

    await call.message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
        reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(f'{condition}',
                              reply_markup=logic_menu_inline.get_inline_logic_problems_category_info(info_problem))

    await call.answer()


async def tasks_category_logic_print_info(call: types.CallbackQuery, callback_data: dict):
    translate = callback_data['translate_logic']

    for i in range(len(problems_info_data_logic)):
        if translate in problems_info_data_logic[i]:
            await call.message.answer(f'{problems_info_data_logic[i]}')
            break
    await call.answer()


def register_handlers_tasks_logic_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_logic_start, Text(equals="Задания из категории Логика"))

    all_files_names = [i[0] for i in finding_categories_table('logic')]
    dp.register_callback_query_handler(tasks_category_logic_print,
                                       callback_problems_logic.filter(category_logic=all_files_names), state='*')

    info = ['Solution 1', 'Solution 2', 'Decision', 'Answer', 'Hint', 'Remarks']
    dp.register_callback_query_handler(tasks_category_logic_print_info,
                                       callback_problems_info_logic.filter(info_logic=info), state='*')
