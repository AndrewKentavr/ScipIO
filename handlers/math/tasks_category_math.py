import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from data_b.dp_control import problem_category_random, finding_categories_table
from handlers.keyboards.default import math_menu
from handlers.keyboards.inline import math_menu_inline

callback_problems_math = CallbackData("problems", "category")
callback_problems_info_math = CallbackData("values", "info", "translate")


async def tasks_category_math_start(message: types.Message):
    await message.answer('Выберите категорию заданий:',
                         reply_markup=math_menu_inline.get_inline_math_problems_category())


async def tasks_category_math_print_inline(call: types.CallbackQuery, callback_data: dict):
    global category
    category = callback_data["category"]
    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    dictionary_info_problem = problem_category_random(category, 'math')

    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])

    global problems_info_data_math
    problems_info_data_math = info_problem

    await call.message.answer(
        f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
        reply_markup=math_menu.get_keyboard_math_category())
    await call.message.answer(f'{condition}',
                              reply_markup=math_menu_inline.get_inline_math_problems_category_info(info_problem))

    await call.answer()


async def tasks_category_math_print_keyboard_default(message: types.Message):
    dictionary_info_problem = problem_category_random(category, 'math')

    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    info_problem = dict(list(dictionary_info_problem.items())[6:])

    global problems_info_data_math
    problems_info_data_math = info_problem

    try:
        await message.answer(
            f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
            reply_markup=math_menu.get_keyboard_math_category())
        await message.answer(f'{condition}',
                             reply_markup=math_menu_inline.get_inline_math_problems_category_info(info_problem))
    except Exception:
        await message.answer('Сломанная задача')


async def tasks_category_math_print_info(call: types.CallbackQuery, callback_data: dict):
    """
    ВОТ ТУТ НУЖНО ИСПРАВЛЯТЬ, Т.К ТУТ НЕПОНЯТНО ЗАЧЕМ НУЖЕН TRANSLATE, ЕСЛИ ЕСТЬ info_math
    """

    translate = callback_data['translate']
    try:
        if translate == 'Решение 1':
            await call.message.answer(f'{problems_info_data_math["decisions_1"]}')

        elif translate == 'Решение 2':
            await call.message.answer(f'{problems_info_data_math["decisions_2"]}')
        elif translate == 'Ответ':
            await call.message.answer(f'{problems_info_data_math["answer"]}')
        elif translate == 'Замечания':
            await call.message.answer(f'{problems_info_data_math["remarks"]}')

    except Exception:
        await call.message.answer(f'Ответ не выводится')

    await call.answer()


async def tasks_category_math_end(message: types.Message, state: FSMContext):

    await state.finish()
    await message.answer(emoji.emojize(":red_circle: ") + 'Выполнение задачек закончилось',
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_tasks_math_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_math_start, Text(equals="Задания из категорий Математики"))

    all_files_names = [i[0] for i in finding_categories_table('math')]
    dp.register_callback_query_handler(tasks_category_math_print_inline,
                                       callback_problems_math.filter(category=all_files_names), state='*')

    dp.register_message_handler(tasks_category_math_print_keyboard_default, Text(equals="Следующая задача"))
    dp.register_message_handler(tasks_category_math_end, Text(equals="Закончить математику"))

    info = ['Decision 1', 'Decision 2', 'Answer', 'Remarks']
    dp.register_callback_query_handler(tasks_category_math_print_info,
                                       callback_problems_info_math.filter(info=info), state='*')
