from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from dp.dp_math import problem_search_random
from handlers.keyboards.default import math_menu


async def math_problems_start(message: types.Message):
    await message.answer('Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
    await Problems.math_problems.set()


async def math_problems(message: types.Message, state: FSMContext):
    c = problem_search_random()
    condition_dp = c[1]
    answer_dp = c[2]
    if c[3]:
        explanation = c[3]

    print(answer_dp)

    user_data = await state.get_data()

    if len(user_data) == 0:
        await state.update_data(condition=[])
        await state.update_data(answer=[])
        await state.update_data(attempts=[])
        user_data = await state.get_data()
    answers = user_data['answer']
    answers.append(answer_dp)

    conditions = user_data['condition']
    conditions.append(condition_dp)

    attempt = user_data['attempts']
    attempt.append(0)

    await state.update_data(condition=conditions)
    await state.update_data(answer=answers)
    await state.update_data(attempts=attempt)

    await message.answer(f'Решите данную задачу:\n{condition_dp}', reply_markup=types.ReplyKeyboardRemove())
    await Problems.next()


async def math_problems_answer(message: types.Message, state: FSMContext):
    try:
        answer_input = int(message.text)
    except ValueError:
        await message.answer(f'Неправильные знаки')
    else:
        user_data = await state.get_data()
        answer = user_data['answer'][-1]
        if int(answer) != answer_input:
            attempt = user_data['attempts']
            cc = attempt[-1] + 1
            attempt[-1] = cc
            await state.update_data(attempts=attempt)

            await message.answer('Не правильно\nПопробуйте ещё раз')
            return
        else:
            await message.answer('Правильно, вы молодцы!!')
            await Problems.math_problems.set()
            await message.answer('Что делаем?', reply_markup=math_menu.get_keyboard_math_end_problem())


async def math_problems_end(message: types.Message, state: FSMContext):
    await message.answer('НУ и закончил', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()

    conditions = user_data['condition']
    answer = user_data['answer']
    attempt = user_data['attempts']

    for i in range(len(conditions)):
        await message.answer(
            f'Условие задачи:\n{conditions[i]}\n    Ответ: {answer[i]}\n    Количество попыток: {attempt[i]}')
    await state.finish()


class Problems(StatesGroup):
    math_problems = State()
    math_problems_answer = State()


def register_handlers_math_problem(dp: Dispatcher):
    dp.register_message_handler(math_problems_start, Text(equals="Задачки"))
    dp.register_message_handler(math_problems_start, commands="math_problems")
    dp.register_message_handler(math_problems_end, Text(equals="закончить задачки", ignore_case=True), state="*")
    dp.register_message_handler(math_problems, state=Problems.math_problems)
    dp.register_message_handler(math_problems_answer, state=Problems.math_problems_answer)
