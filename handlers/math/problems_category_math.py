import os

from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from data_b.dp_math import problem_category_random
from handlers.keyboards.inline import math_menu_inline

callback_problems = CallbackData("problems", "category")
callback_problems_info = CallbackData("values", "info", "translate")


async def problems_category_start(message: types.Message):
    await message.answer('Выберете категорию заданий:',
                         reply_markup=math_menu_inline.get_inline_math_problems_category())


async def problems_category_print(call: types.CallbackQuery, callback_data: dict):
    category = callback_data["category"]
    list_info_problem = problem_category_random(category)
    title = list_info_problem[0]
    href = list_info_problem[1]
    subcategory = list_info_problem[2]
    complexity, classes = list_info_problem[3], list_info_problem[4]
    condition = list_info_problem[5]
    info_problem = list_info_problem[6:]
    global problems_info_data
    problems_info_data = info_problem

    await call.message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}')
    await call.message.answer(f'{condition}',
                              reply_markup=math_menu_inline.get_inline_math_problems_category_info(info_problem))

    await call.answer()


async def problems_category_print_info(call: types.CallbackQuery, callback_data: dict):
    translate = callback_data['translate']

    for i in range(len(problems_info_data)):
        if translate in problems_info_data[i]:
            await call.message.answer(f'{problems_info_data[i]}')
            break
    await call.answer()


def register_handlers_math_problem_category(dp: Dispatcher):
    dp.register_message_handler(problems_category_start, Text(equals="Задания по категориям"))
    dp.register_message_handler(problems_category_start, commands="problems_category")

    all_files_names = os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json")
    all_file_names_list_not_json = [file_name_json.split('.json')[0] for file_name_json in all_files_names]
    dp.register_callback_query_handler(problems_category_print,
                                       callback_problems.filter(category=all_file_names_list_not_json), state='*')

    info = ['Solution 1', 'Solution 2', 'Decision', 'Answer', 'Hint', 'Remarks']
    dp.register_callback_query_handler(problems_category_print_info,
                                       callback_problems_info.filter(info=info), state='*')
