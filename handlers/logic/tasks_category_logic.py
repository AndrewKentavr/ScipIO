from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink

from data_b.dp_control import problem_category_random, finding_categories_table, action_add
from handlers.keyboards.default import logic_menu
from handlers.logic.logic import LogicButCategory

callback_problems_logic = CallbackData("problems_logic", "category_logic")
callback_problems_info_logic = CallbackData("values_logic", "info_logic", "translate_logic")


async def tasks_category_logic_start(message: types.Message, state: FSMContext):
    from handlers.keyboards.inline import logic_menu_inline

    await state.update_data(correct=[])

    await message.answer('Выберите категорию заданий:',
                         reply_markup=logic_menu_inline.get_inline_logic_problems_category())

    link_endrey = hlink('в этот телеграм', 'https://t.me/Endrey_k')
    await message.answer(f'<u>Если задание неправильное или неправильно выводиться, то прошу написать {link_endrey}</u>'
                         ' сообщение вида:\n'
                         '(категория) - (id задачи или название) - (и часть условия)\n'
                         'Например: Математика - 35793 - Дан тетраэдр, у которого пери...',
                         disable_web_page_preview=True)
    await LogicCategory.logic_step.set()


async def tasks_category_logic_print_keyboard_inline(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # НУЖНЫ ИЗМЕНЕНИЯ В КОММЕНТАРИИ

    """
    :param call: Это ответ на нажатие INLINE кнопки КАТЕГОРИЯ
    :param callback_data: Это значения INLINE кнопки, то есть это информация
    о категории (её вроде бы info_logic, translate_logic)
    :return:
    """
    from handlers.keyboards.inline import logic_menu_inline

    # объявлен global, чтобы при нажатии "Следующее задание" выводило туже категорию

    await state.update_data(category=callback_data["category_logic"])

    category = callback_data["category_logic"]
    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    dictionary_info_problem = problem_category_random(category, 'logic')

    id = dictionary_info_problem['id']
    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']
    if str(title) == 'None':
        title = id
    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])

    await state.update_data(problems_info_data_logic=info_problem)

    link_problems = hlink('Ссылка на задачу', href)
    dop_info = f'\nПодкатегория: {subcategory}\nСложность: {complexity}\nКлассы: {classes}'
    await call.message.answer(
        f'Название задания или его ID: {title}\n{link_problems}',
        reply_markup=logic_menu.get_keyboard_logic_category(), disable_web_page_preview=True)
    await call.message.answer(f'{condition}',
                              reply_markup=logic_menu_inline.get_inline_logic_problems_category_info(info_problem))

    await call.answer()


async def tasks_category_logic_print_keyboard_default(message: types.Message, state: FSMContext):
    from handlers.keyboards.inline import logic_menu_inline
    user_data = await state.get_data()
    # Берёт из бд рандомную задачу и данные хранятся в СЛОВАРЕ
    category = user_data['category']
    dictionary_info_problem = problem_category_random(category, 'logic')

    id = dictionary_info_problem['id']
    title = dictionary_info_problem['title']
    href = dictionary_info_problem['href']
    subcategory = dictionary_info_problem['subcategory']
    complexity, classes = dictionary_info_problem['complexity'], dictionary_info_problem['classes']
    condition = dictionary_info_problem['conditions']

    # если "правильно", то в user_data['correct'] добавляется id карточки
    if message.text == emoji.emojize(":white_check_mark:") + ' Правильно':
        correct = user_data['correct']
        # Если названия задачки не существует, то в вывод подается не название задача и id задачи
        if title == 'None':
            correct.append(id)
        else:
            correct.append(title)
        correct.append(href)
        await state.update_data(correct=correct)

        # добавление action cat_logic в бд
        action_add(message.from_user.id, 'cat_logic', True)
    else:
        action_add(message.from_user.id, 'cat_logic', False)

    # Образка словаря
    info_problem = dict(list(dictionary_info_problem.items())[6:])

    await state.update_data(problems_info_data_logic=info_problem)

    if str(title) == 'None':
        title = id

    link_problems = hlink('Ссылка на задачу', href)
    # В задачках логики нет сложности, классов и подкатегорий, поэтому вынес в отдельную переменную
    dop_info = f'\nПодкатегория: {subcategory}\nСложность: {complexity}\nКлассы: {classes}'
    await message.answer(
        f'Название задания или его ID: {title}\n{link_problems}',
        reply_markup=logic_menu.get_keyboard_logic_category(), disable_web_page_preview=True)
    await message.answer(f'{condition}',
                         reply_markup=logic_menu_inline.get_inline_logic_problems_category_info(info_problem))


async def tasks_category_logic_print_info(call: types.CallbackQuery, callback_data: dict, state:FSMContext):
    """
    ВОТ ТУТ НУЖНО ИСПРАВЛЯТЬ, Т.К ТУТ НЕПОНЯТНО ЗАЧЕМ НУЖЕН TRANSLATE, ЕСЛИ ЕСТЬ info_logic
    """
    user_data = await state.get_data()
    problems_info_data_logic = user_data['problems_info_data_logic']
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


async def tasks_category_logic_end(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    # Список correct содержит id задач и сразу после id идет ссылка на задачу
    correct = user_data['correct']
    await state.finish()
    string_correct = ''
    count = 1
    # Создание статистики
    for i in range(0, len(correct), 2):
        link_problems = hlink('Ссылка на задачу', correct[i + 1])
        string_correct += f"{count}: id - {correct[i]} ({link_problems})\n"
        count += 1

    await message.answer(
        emoji.emojize(":bar_chart:") + f"Количество правильно решённых задач: {len(correct) // 2}\n{string_correct}",
        disable_web_page_preview=True)

    await message.answer(emoji.emojize(":red_circle: ") + ' Выполнение задачек закончилось',
                         reply_markup=types.ReplyKeyboardRemove())


class LogicCategory(StatesGroup):
    """Данные state нужен, чтобы отделять одинаковые кнопки 'Закончить' и 'Следующая задача'"""
    logic_step = State()


def register_handlers_tasks_logic_category(dp: Dispatcher):
    dp.register_message_handler(tasks_category_logic_start,
                                Text(equals=emoji.emojize(":book:") + ' Задания из категорий'),
                                state=LogicButCategory.logic_category_step)

    all_files_names = [i[0] for i in finding_categories_table('logic')]
    dp.register_callback_query_handler(tasks_category_logic_print_keyboard_inline,
                                       callback_problems_logic.filter(category_logic=all_files_names), state='*')
    choose = [emoji.emojize(":white_check_mark:") + ' Правильно', emoji.emojize(":x:") + ' Неправильно']
    dp.register_message_handler(tasks_category_logic_print_keyboard_default,
                                Text(choose),
                                state=LogicCategory.logic_step)
    dp.register_message_handler(tasks_category_logic_end,
                                Text(equals=emoji.emojize(":stop_sign:") + ' Закончить'),
                                state=LogicCategory.logic_step)

    info = ['Decision 1', 'Decision 2', 'Answer', 'Remarks']
    dp.register_callback_query_handler(tasks_category_logic_print_info,
                                       callback_problems_info_logic.filter(info_logic=info), state='*')
