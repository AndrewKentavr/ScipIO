from random import choice, randint
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.keyboards.default.keyboard_menu import get_keyboard_math_start


async def math_start(message: types.Message):
    await message.answer('Выберете:', reply_markup=get_keyboard_math_start())


async def equation_mentally_start(message: types.Message):
    await message.answer('Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
    await Equation.equation_mentally.set()


async def equation_mentally(message: types.Message, state: FSMContext):
    equation = equation_generate()
    await state.update_data(answer=equation[1])
    await message.answer(f'Решите в уме:\n{equation[0]}')
    await Equation.next()


async def equation_mentally_answer(message: types.Message, state: FSMContext):
    try:
        answer_input = int(message.text)
    except ValueError:
        await message.answer(f'Неправильные знаки')
    else:
        user_data = await state.get_data()
        answer = user_data['answer']
        if int(answer) != answer_input:
            await message.answer('Не правильно\nПопробуйте ещё раз')
            return
        else:
            await message.answer('Правильно, вы молодцы!!')
            await state.finish()
            await Equation.equation_mentally.set()
            await message.answer('Ещё?')


def equation_generate():
    mathematically_signs = ['*']
    sign = choice(mathematically_signs)
    A = str(randint(11, 99))
    B = str(randint(11, 99))
    equation = f'{A} {sign} {B}'
    answer = eval(equation)

    return [equation, answer]


class Equation(StatesGroup):
    equation_mentally = State()
    equation_mentally_answer = State()


def register_handlers_math(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='math', state="*")
    dp.register_message_handler(equation_mentally_start, Text(equals="Примеры для подчёта в уме"))
    dp.register_message_handler(equation_mentally_start, commands="equation_mentally")
    dp.register_message_handler(equation_mentally, state=Equation.equation_mentally)
    dp.register_message_handler(equation_mentally_answer, state=Equation.equation_mentally_answer)
