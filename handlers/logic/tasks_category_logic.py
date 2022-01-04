from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from pymystem3 import Mystem

from data_b.dp_control import problem_category_random, finding_categories_table

callback_problems_logic = CallbackData("problems_logic", "category_logic")
callback_problems_info_logic = CallbackData("values_logic", "info_logic", "translate_logic")


async def tasks_category_logic_start(message: types.Message):
    from handlers.keyboards.default import logic_menu_second

    await message.answer('Выберете категорию заданий:',
                         reply_markup=logic_menu_second.get_inline_logic_problems_category())


async def tasks_category_logic_print(call: types.CallbackQuery, callback_data: dict):
    from handlers.keyboards.default import logic_menu_second

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
    global answer
    answer = problems_info_data_logic[2]

    await call.message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
        reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(f'{condition}',
                              reply_markup=logic_menu_second.get_inline_logic_problems_category_info(info_problem))
    await Logic_Answer.Waiting_User_Choise.set()


async def answer_checker_step_one(message: types.Message):
    await message.answer('Введите ваш ответ:')
    await Logic_Answer.Waiting_Answer.set()


async def answer_checker_step_two(message: types.Message):
    mystem = Mystem()
    lemmatized_message_text = mystem.lemmatize(message.text)
    lemmatized_answer_text = mystem.lemmatize(problems_info_data_logic[2])
    lemmatized_solution_text = mystem.lemmatize(problems_info_data_logic[0])
    answer_is_right = False
    for i in range(len(lemmatized_message_text) - 1):
        if (lemmatized_message_text[i] in lemmatized_answer_text or lemmatized_message_text[i] in lemmatized_solution_text) and lemmatized_message_text[i] != ' ' and lemmatized_message_text[i] != "\n" and lemmatized_message_text[i] != 'ответ':
            await message.answer('Правильно!')
            answer_is_right = True
            await Logic_Answer.next()
            await Logic_Answer.next()
            break
    if not answer_is_right:
        await message.answer('К сожалению пока неверно, подумайте ещё.')
        await Logic_Answer.next()


async def tasks_category_logic_print_answer(message: types.CallbackQuery):
    await message.answer(f'{problems_info_data_logic[2]}')
    await Logic_Answer.next()


async def tasks_category_logic_print_solution1(message: types.CallbackQuery):
    await message.answer(f'{problems_info_data_logic[0]}')
    await Logic_Answer.next()


async def tasks_category_logic_print_hint(message: types.CallbackQuery):
    await message.answer(f'{problems_info_data_logic[3]}')


class Logic_Answer(StatesGroup):
    Waiting_Answer = State()
    Waiting_User_Choise = State()


def register_handlers_tasks_logic_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_logic_start, Text(equals="Задания по категориям Логики"))
    all_files_names = [i[0] for i in finding_categories_table('logic')]
    dp.register_callback_query_handler(tasks_category_logic_print,
                                       callback_problems_logic.filter(category_logic=all_files_names), state='*')
    dp.register_message_handler(answer_checker_step_one, Text(equals="Ответить"),
                                state=Logic_Answer.Waiting_User_Choise)
    dp.register_message_handler(answer_checker_step_two, state=Logic_Answer.Waiting_Answer)
    info = ['Solution 1', 'Solution 2', 'Decision', 'Answer', 'Hint', 'Remarks', 'check_answer']
    dp.register_message_handler(tasks_category_logic_print_answer, Text(equals='Посмотреть ответ'),
                                state=Logic_Answer.Waiting_User_Choise)
    dp.register_message_handler(tasks_category_logic_print_solution1, Text(equals='Решение'),
                                state=Logic_Answer.Waiting_User_Choise)
    dp.register_message_handler(tasks_category_logic_print_hint, Text(equals='Подсказка'),
                                state=Logic_Answer.Waiting_User_Choise)
