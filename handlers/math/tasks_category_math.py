from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink

from data_b.dp_control import problem_category_random, finding_categories_table, finding_one_categories_table, \
    finding_main_categories_table
from handlers.keyboards.default import math_menu
from handlers.keyboards.inline import math_menu_inline
from handlers.math.math import MathButCategory
import pyshorteners

callback_problems_math = CallbackData("problems", "category")
callback_problems_info_math = CallbackData("values", "info", "translate")
callback_main_problems_math = CallbackData("problems", "category")


async def tasks_category_math_start(message: types.Message, state: FSMContext):
    await state.update_data(correct=[])
    await message.answer('Выберите категорию заданий:',
                         reply_markup=math_menu_inline.get_inline_main_math_problems_category())
    link_endrey = hlink('в этот телеграм', 'https://t.me/Endrey_k')
    await message.answer(f'<u>Если задание неправильное или неправильно выводиться, то прошу написать {link_endrey}</u>'
                         ' сообщение вида:\n'
                         '(категория) - (id задачи или название) - (и часть условия)\n'
                         'Например: Математика - 35793 - Дан тетраэдр, у которого пери...')


async def one_tasks_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    categories = finding_one_categories_table(call["data"][9:])
    if len(categories) == 1:
        global category
        category = callback_data["category"][:-5]
        # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
        dictionary_info_problem = problem_category_random(category, 'math')

        title = dictionary_info_problem['title']
        href = pyshorteners.Shortener().tinyurl.short(dictionary_info_problem['href'])
        subcategory = dictionary_info_problem['subcategory']
        complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
        condition = dictionary_info_problem['conditions']

        await state.update_data(card_id=href)

        # Образка словаря
        info_problem = dict(list(dictionary_info_problem.items())[6:])

        global problems_info_data_math
        problems_info_data_math = info_problem
        try:
            await call.message.answer(
                f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
                reply_markup=math_menu.get_keyboard_math_category())
            await call.message.answer(f'{condition}',
                                      reply_markup=math_menu_inline.get_inline_math_problems_category_info(
                                          info_problem))

            await call.answer()
            await MathCategory.math_step.set()

        except Exception:
            await call.message.answer('Сломанная задача')
    else:
        await call.answer()
        await call.message.answer('Выберите подкатегорию заданий:',
                                  reply_markup=math_menu_inline.get_inline_one_main_math_problems_category(
                                      callback_data["category"]))


async def tasks_category_math_print_inline(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    global category
    category = callback_data["category"]
    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    dictionary_info_problem = problem_category_random(category, 'math')

    title = dictionary_info_problem['title']
    href = pyshorteners.Shortener().tinyurl.short(dictionary_info_problem['href'])
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    await state.update_data(card_id=href)

    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])

    global problems_info_data_math
    problems_info_data_math = info_problem
    try:
        await call.message.answer(
            f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
            reply_markup=math_menu.get_keyboard_math_category())
        await call.message.answer(f'{condition}',
                                  reply_markup=math_menu_inline.get_inline_math_problems_category_info(info_problem))

        await call.answer()
        await MathCategory.math_step.set()

    except Exception:
        await call.message.answer('Сломанная задача')


async def tasks_category_math_print_keyboard_default(message: types.Message, state: FSMContext):
    dictionary_info_problem = problem_category_random(category, 'math')

    title = dictionary_info_problem['title']
    href = pyshorteners.Shortener().tinyurl.short(dictionary_info_problem['href'])
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    await state.update_data(card_id=href)

    info_problem = dict(list(dictionary_info_problem.items())[6:])

    global problems_info_data_math
    problems_info_data_math = info_problem

    try:
        if message.text == emoji.emojize(":white_check_mark:") + ' Правильно':
            user_data = await state.get_data()
            # если "правильно", то в user_data['correct'] добавляется id карточки
            correct = user_data['correct']
            correct.append(user_data['card_id'])
            await state.update_data(correct=correct)
        await message.answer(
            f'Название задания или его ID: {title}\nСсылка на задание: {href}\nПодкатегория: {subcategory}\n{complexity}, {classes}',
            reply_markup=math_menu.get_keyboard_math_category())
        await message.answer(f'{condition}',
                             reply_markup=math_menu_inline.get_inline_math_problems_category_info(info_problem))
        await MathCategory.math_step.set()

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

    user_data = await state.get_data()
    correct = user_data['correct']
    await state.finish()
    string_correct = ''
    for i in range(len(correct)):
        string_correct += f"{i + 1}: id - {correct[i][52:]} ({pyshorteners.Shortener().tinyurl.short(correct[i])})\n"

    await message.answer(emoji.emojize(":bar_chart:") + f"Количество правильно решённых задач: {len(correct)}\n{string_correct}")

    await message.answer(emoji.emojize(":red_circle: ") + ' Выполнение задачек закончилось',
                         reply_markup=types.ReplyKeyboardRemove())


class MathCategory(StatesGroup):
    """Данные state нужен, чтобы отделять одинаковые кнопки 'Закончить' и 'Следующая задача'"""
    math_step = State()
    math_choose = State()


def register_handlers_tasks_math_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_math_start,
                                Text(equals=emoji.emojize(":book:") + ' Задания из категорий'),
                                state=MathButCategory.math_category_step)

    all_main_files_names = [i[0] for i in finding_main_categories_table('math')]
    dp.register_callback_query_handler(one_tasks_category,
                                       callback_main_problems_math.filter(category=all_main_files_names), state='*')

    all_files_names = [i[0] for i in finding_categories_table('math')]
    dp.register_callback_query_handler(tasks_category_math_print_inline,
                                       callback_problems_math.filter(category=all_files_names), state='*')

    choose = [emoji.emojize(":white_check_mark:") + ' Правильно', emoji.emojize(":x:") + ' Неправильно']
    dp.register_message_handler(tasks_category_math_print_keyboard_default,
                                Text(choose),
                                state=MathCategory.math_step)
    dp.register_message_handler(tasks_category_math_end,
                                Text(equals=emoji.emojize(":stop_sign:") + ' Закончить'),
                                state=MathCategory.math_step)

    info = ['Decision 1', 'Decision 2', 'Answer', 'Remarks']
    dp.register_callback_query_handler(tasks_category_math_print_info,
                                       callback_problems_info_math.filter(info=info), state='*')
