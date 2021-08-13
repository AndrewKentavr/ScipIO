from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from data_b.dp_math import formulas_search_random
from handlers.keyboards.default.math_menu import get_keyboard_math_formulas
from handlers.keyboards.inline.math_menu_inline import get_inline_math_formulas


async def math_formulas_start(message: types.Message):
    await message.answer('Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
    await Formulas.math_formulas.set()


async def math_formulas(message: types.Message, state: FSMContext):
    c = formulas_search_random()
    condition_dp = c[0]
    answer_dp = c[1]

    user_data = await state.get_data()

    if len(user_data) == 0:
        await state.update_data(explanation=[])
        await state.update_data(condition=[])
        await state.update_data(answer=[])
        user_data = await state.get_data()

    if c[2]:
        explanation_dp = c[2]
        explanations = user_data['explanation']
        explanations.append(explanation_dp)
        await state.update_data(explanation=explanations)

    answers = user_data['answer']
    answers.append(answer_dp)

    conditions = user_data['condition']
    conditions.append(condition_dp)

    await state.update_data(condition=conditions)
    await state.update_data(answer=answers)
    await state.finish()

    await message.answer(f"Формула:\n{str(condition_dp)}", reply_markup=get_inline_math_formulas())
    # await message.answer(f'Посмотрите Продолжить или закончить?', reply_markup=get_keyboard_math_formulas(), )


async def hint_func(call: types.CallbackQuery):
    # user_data = await state.get_data()
    # explanation = user_data['explanation'][-1]
    #
    # await call.message.answer(f'Вот объяснение:\n{explanation}')
    await call.message.answer(f'111111111111111')
    await call.answer()


async def answer_func(call: types.CallbackQuery):
    # user_data = await state.get_data()
    # answer = user_data['answer'][-1]

    # await call.message.answer(f'Вот ответ:\n{answer}')
    await call.message.answer(f'2222222222222222')
    await call.answer()


async def math_formulas_end(message: types.Message, state: FSMContext):
    await message.answer('НУ и закончил', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()

    conditions = user_data['condition']
    answer = user_data['answer']

    for i in range(len(conditions)):
        await message.answer(
            f'Условие задачи:\n{conditions[i]}\n    Ответ: {answer[i]}\n')
    await state.finish()


class Formulas(StatesGroup):
    math_formulas = State()


def register_handlers_math_formulas(dp: Dispatcher):
    dp.register_message_handler(math_formulas_start, Text(equals="Формулы"))
    dp.register_message_handler(math_formulas_start, commands="math_formulas")
    dp.register_message_handler(math_formulas_end, Text(equals="закончить задачки", ignore_case=True), state="*")
    dp.register_message_handler(math_formulas, state=Formulas.math_formulas)
    dp.register_callback_query_handler(hint_func, text="hint_f")
    dp.register_callback_query_handler(answer_func, text="answer_f")


def register_handlers_math_formulas_inline(dp: Dispatcher):
    # dp.register_callback_query_handler(hint_func, text="hint_f")
    # dp.register_callback_query_handler(answer_func, text="answer_f")
    pass
