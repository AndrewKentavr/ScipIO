import os

from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from handlers.keyboards.inline import math_menu_inline

callback_problems = CallbackData("problems", "category")


async def problems_category_start(message: types.Message):
    await message.answer('Выберете категорию заданий:',
                         reply_markup=math_menu_inline.get_inline_math_problems_category())


async def problems_category_print(call: types.CallbackQuery, callback_data: dict):
    category = callback_data["category"]

    await call.message.answer(f'{category}')
    await call.answer()


def register_handlers_math_problem_category(dp: Dispatcher):
    dp.register_message_handler(problems_category_start, Text(equals="Задания по категориям"))
    dp.register_message_handler(problems_category_start, commands="problems_category")
    all_files_names = os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json")
    all_file_names_list_not_json = [file_name_json.split('.json')[0] for file_name_json in all_files_names]

    dp.register_callback_query_handler(problems_category_print,
                                       callback_problems.filter(category=all_file_names_list_not_json), state='*')
