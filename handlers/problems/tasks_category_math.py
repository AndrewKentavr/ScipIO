"""
Основная идея алгоритма в том чтобы отправлять задачи пользвателю после того как он нажмет "Правильно" или "Неправильно".

Сначал пользователю предоставляется выбор основной категории(функция: tasks_category_math_start), после того как пользователь выберет основную категори
    пользователь должен будет выбрать подкатегрию(функция: one_tasks_category), если подкатегории нет, то пользователю сразу присылется задача.

Основной алгоритм:
    1) Предоставляется выбор основной категории. Функция: tasks_category_math_start
    2) Проверка есть ли подкатегория. Если подкатегории нет, то задача отправляется сразу. Если подкатегория есть
    то пользователь выбирает подкатегорию. Функция: one_tasks_category
    3) После выбора подкатегории, пользователю отправляется первая задача. Функция: tasks_category_math_print_keyboard_inline
    4) Когда пользователь ответит "Правильно" или "Неправильно" то вызывается функция: tasks_category_math_print_keyboard_default
    5) Чтобы закончить решение задач, пользователь может прописать "Закончить математику"

"""
import html
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import emoji
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink

from database.dp_control import problem_category_random, action_add
from database import dp_control
from handlers.keyboards.default import math_menu
from handlers.keyboards.inline import math_menu_inline
from handlers.problems.math import MathButCategory
from handlers.problems.logic import LogicButCategory

callback_problems_math = CallbackData("problems", "category")
callback_problems_info_math = CallbackData("values", "info")
callback_main_problems_math = CallbackData("problems", "category")


# Отправляет список категорий
async def tasks_category_math_start(message: types.Message, state: FSMContext):
    step = await state.get_state()  # problems or logic

    if step == MathButCategory.math_category_step.state:
        type_problem = "math"
    elif step == LogicButCategory.logic_category_step.state:
        type_problem = "logic"

    await state.update_data(correct=[])

    await message.answer('Выберите категорию заданий:',
                         reply_markup=math_menu_inline.get_math_categories(type_problem))
    # link_endrey = hlink('в этот телеграм', 'https://t.me/Endrey_k')
    # await message.answer(f'<u>Если задание неправильное или неправильно выводиться, то прошу написать {link_endrey}</u>'
    #                      ' сообщение вида:\n'
    #                      '(категория) - (id задачи или название) - (и часть условия)\n'
    #                      'Например: Математика - 35793 - Дан тетраэдр, у которого пери...',
    #                      disable_web_page_preview=True)


# Отправляет список категорий. Если подкатегорий нет, отправляет задачу
async def one_tasks_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    categories = dp_control.get_math_categories(callback_data["category"])
    if len(categories) == 0:
        category = callback_data["category"]
        await state.update_data(category=category)
        # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
        await send_math_problem(category, call, state)  # отправляет задачу пользователю
        await call.answer()
    else:
        await call.answer()
        await call.message.answer('Выберите подкатегорию заданий:',
                                  reply_markup=math_menu_inline.get_math_categories(callback_data["category"]))


# Отвечает на кнопки ПРАВИЛЬНО и НЕПРАВИЛЬНО, после чего отправляет задачу
async def tasks_category_math_print_keyboard_default(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category = user_data['category']
    await send_math_problem(category, message, state)

    # если "правильно", то в user_data['correct'] добавляется id карточки
    if message.text == emoji.emojize(":white_check_mark:") + ' Правильно':
        user_data = await state.get_data()
        correct = user_data['correct']
        href = user_data["info_problem"]["href"]
        step = await state.get_state()  # problems or logic

        if step == MathButCategory.math_category_step.state:
            correct.append([user_data["info_problem"]["title"], user_data["info_problem"]["href"]])
        elif step == LogicButCategory.logic_category_step.state:
            if user_data["info_problem"]["title"] == 'None':
                correct.append([user_data["info_problem"]["id"], user_data["info_problem"]["href"]])
            else:
                correct.append([user_data["info_problem"]["title"], user_data["info_problem"]["href"]])

        await state.update_data(correct=correct)

        # добавление action cat_math в бд
        action_add(message.from_user.id, 'cat_math', True)
    else:
        action_add(message.from_user.id, 'cat_math', False)


# Отвечает на нажатие кнопок под задачей(Ответ, Решение и тд)
async def tasks_category_math_print_info(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_data = await state.get_data()
    info_problem = user_data["info_problem"]
    text = info_problem[callback_data["info"]]
    title = info_problem["title"]
    img = [int(re.search(r'\d+', m).group()) for m in re.findall(r'\[рис \d+\]', text)]
    try:
        if len(img) == 1:
            with open(f"data/math_img/{title}-{img[0]}.jpg", "rb") as photo:
                await call.message.answer_photo(photo=photo)
        elif len(img) > 1:
            media = [types.InputMediaPhoto(open(f"data/math_img/{title}-{p}.jpg", "rb")) for p in img]
            await call.message.answer_media_group(media)
        await call.message.answer(rf'{html.escape(text)}', parse_mode=None)

    except Exception as err:
        await call.message.answer(f'Ответ не выводится')

    await call.answer()


# Отвечает на кнопку закончить и отправляет список решенных задач
async def tasks_category_math_end(message: types.Message, state: FSMContext):
    step = await state.get_state()  # problems or logic

    user_data = await state.get_data()
    # Список correct содержит ссылки на задачи(в каждой ссылке есть id задачи)
    correct = user_data['correct']
    string_correct = ''
    # Создание статистики

    for i in range(len(correct)):
        link_problems = hlink('Ссылка на задачу', correct[i][1])
        string_correct += f"{i + 1}: id - {correct[i][0]} ({link_problems})\n"

    await message.answer(
        emoji.emojize(
            ":bar_chart:") + f"Количество правильно решённых задач: {len(correct)}\n{string_correct}",
        disable_web_page_preview=True)

    await message.answer(emoji.emojize(":red_circle: ") + ' Выполнение задачек закончилось',
                         reply_markup=math_menu.get_keyboard_math_start(message))


async def show_img(message: types.Message):
    dp_control.show_img(message)
    text = ""
    if "Включить" in message.text:
        text = "Задачи с фотографиями включены"
    elif "Выключить" in message.text:
        text = "Задачи с фотографиями отключены"
    await message.answer(text, reply_markup=math_menu.get_keyboard_math_start(message))


def register_handlers_tasks_math_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_math_start,
                                Text(equals=emoji.emojize(":book:") + ' Задания из категорий'),
                                state=[MathButCategory.math_category_step, LogicButCategory.logic_category_step])

    all_main_files_names = [i[0] for i in dp_control.get_math_categories('*')]
    dp.register_callback_query_handler(one_tasks_category,
                                       callback_main_problems_math.filter(category=all_main_files_names), state='*')

    choose = [emoji.emojize(":white_check_mark:") + ' Правильно', emoji.emojize(":x:") + ' Неправильно']
    dp.register_message_handler(tasks_category_math_print_keyboard_default,
                                Text(choose),
                                state=[MathButCategory.math_category_step, LogicButCategory.logic_category_step])

    dp.register_message_handler(tasks_category_math_end,
                                Text(equals=emoji.emojize(":stop_sign:") + ' Закончить'),
                                state=[MathButCategory.math_category_step, LogicButCategory.logic_category_step])

    info = ['decisions_1', 'decisions_2', 'answer', 'remarks']
    dp.register_callback_query_handler(tasks_category_math_print_info,
                                       callback_problems_info_math.filter(info=info), state='*')

    img = [emoji.emojize(":gear:") + ' Выключить задачи с фотографиями',
           emoji.emojize(":gear:") + ' Включить задачи с фотографиями']
    dp.register_message_handler(show_img,
                                Text(img),
                                state=MathButCategory.math_category_step)


async def send_math_problem(category, message, state: FSMContext):
    user_id = message.from_user.id
    if isinstance(message, types.CallbackQuery):
        message = message.message

    step = await state.get_state()
    if step == MathButCategory.math_category_step.state:
        type_problem = "math"
    elif step == LogicButCategory.logic_category_step.state:
        type_problem = "logic"

    img = dp_control.show_img_check(user_id)

    dictionary_info_problem = problem_category_random(category, type_problem, img)
    title = dictionary_info_problem['title']
    if title == 'None':
        title = dictionary_info_problem['id']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    await state.update_data(info_problem=dictionary_info_problem)

    img = [int(re.search(r'\d+', m).group()) for m in re.findall(r'\[рис \d+\]', condition)]

    try:
        link_problems = hlink('Ссылка на задачу', href)

        parts = []
        if subcategory is not None:
            parts.append(f'Подкатегория: {subcategory}')
        if complexity is not None:
            parts.append(f'Сложность: {complexity}')
        if classes is not None:
            parts.append(f'Классы: {classes}')

        dop_info = '\n'.join(parts)

        await message.answer(
            f'Название задания или его ID: {title}\n{link_problems}\n{dop_info}',
            reply_markup=math_menu.get_keyboard_math_category(), disable_web_page_preview=True)
        if len(img) == 1:
            with open(f"data/math_img/{title}-{img[0]}.jpg", "rb") as photo:
                await message.answer_photo(photo=photo)
        elif len(img) > 1:
            media = [types.InputMediaPhoto(open(f"data/math_img/{title}-{p}.jpg", "rb") for p in img)]
            await message.answer_media_group(media)
        await message.answer(f'{condition}',
                             reply_markup=math_menu_inline.get_inline_math_problems_category_info(
                                 dictionary_info_problem))
    except Exception as err:
        await message.answer('Сломанная задача')
