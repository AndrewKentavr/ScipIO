from random import choice, randint
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

from handlers.keyboards.default import math_menu
from handlers.keyboards.inline import math_menu_inline


async def equation_mentally_theory(message: types.Message):
    await message.answer(
        'Мы должны использовать: <b>Круглые Числа</b>\nОдин из самых распространённыхприёмов устного счёта'
        ' заключается в том, что любое число можно представить в виде суммы или разности чисел, одно или '
        'несколько из которых «круглое»', reply_markup=math_menu_inline.get_inline_math_url())
    photo = InputFile("C:/Users/andrt/PycharmProjects/ConTia/data/math_1.jpg")
    await message.answer_photo(photo=photo)
    await message.answer(
        '<b>Упростим умножение делением</b>\nПри устном счёте бывает удобнее оперировать делимым и делителем нежели '
        'целым числом (например, <i>5</i> представлять в виде <i>10:2</i>, а <i>50</i> в виде <i>100:2)</i>:')
    await message.answer(
        '68 x 50 = (68 x 100) : 2 = 6800 : 2 = 3400;\n'
        '3400 : 50 = (3400 x 2) : 100 = 6800 : 100 = 68.')
    await message.answer(
        '625 x 53 = 625 x 50 + 625 x 3 = (625 x 100) : 2 + 600 x 3 + 25 x 3 = (625 x 100) : 2 + 1800 + '
        '(20 + 5) x 3 = (60000 + 2500) : 2 + 1800 + 60 + 15 = 30000 + 1250 + 1800 + 50 + 25 = 33000 + '
        '50 + 50 + 25 = 33125.')
    await message.answer(
        '<b>Возведение в квадрат двузначного числа</b>\nОказывается, чтобы просто возвести любое двузначное число в '
        'квадрат, достаточно запомнить квадраты всех чисел от 1 до 25. Благо, квадраты до 10 мы уже знаем из таблицы '
        'умножения. Остальные квадраты можно посмотреть в нижеприведённой таблице:')

    photo_2 = InputFile("C:/Users/andrt/PycharmProjects/ConTia/data/math_2.jpg")
    await message.answer_photo(photo=photo_2)
    await message.answer(
        '<b>Приём Рачинского</b> заключается в следующем. Для того чтобы найти квадрат любого двузначного числа, надо разность'
        ' между этим числом и <i>25</i> умножить на <i>100</i> и к получившемуся произведению прибавить квадрат '
        'дополнения данного числа до <i>50</i> или квадрат избытка его над <i>50-ю</i>. Например:')
    await message.answer(
        '37^2 = 12 x 100 + 13^2 = 1200 + 169 = 1369;\n84^2 = 59 x 100 + 34^2 = 5900 + 9 x'
        ' 100 + 16^2 = 6800 + 256 = 7056;')


async def equation_mentally_start(message: types.Message):
    await message.answer('Чтобы вызвать подсказку напишите /mell_theory')
    await message.answer('Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
    await Equation.equation_mentally.set()


async def equation_mentally(message: types.Message, state: FSMContext):
    equation = equation_generate()
    user_data = await state.get_data()

    if len(user_data) == 0:
        await state.update_data(answer=[])
        await state.update_data(attempts=[])
        user_data = await state.get_data()
    answers = user_data['answer']
    answers.append(equation[1])

    attempt = user_data['attempts']
    attempt.append(0)

    await state.update_data(answer=answers)
    await state.update_data(attempts=attempt)

    await message.answer(f'Решите в уме:\n{equation[0]}', reply_markup=types.ReplyKeyboardRemove())
    await Equation.next()


async def equation_mentally_answer(message: types.Message, state: FSMContext):
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
            await Equation.equation_mentally.set()
            await message.answer('Что делаем?', reply_markup=math_menu.get_keyboard_math_end())


async def equation_mentally_end(message: types.Message, state: FSMContext):
    await message.answer('НУ и закончил', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    answer = user_data['answer']
    attempt = user_data['attempts']
    await message.answer(f'Ответы: {answer}\nКоличество попыток на каждый ответ: {attempt}')
    await state.finish()


def equation_generate():
    mathematically_signs = ['*']
    sign = choice(mathematically_signs)
    A = str(randint(11, 99))
    B = str(randint(11, 99))
    equation = f'{A} {sign} {B}'
    answer = eval(equation)
    print(answer)

    return [equation, answer]


class Equation(StatesGroup):
    equation_mentally = State()
    equation_mentally_answer = State()


def register_handlers_math_mentally(dp: Dispatcher):
    dp.register_message_handler(equation_mentally_theory, commands='mell_theory', state='*')
    dp.register_message_handler(equation_mentally_end, Text(equals="закончить", ignore_case=True), state="*")

    dp.register_message_handler(equation_mentally_start, Text(equals="Примеры для подчёта в уме"))
    dp.register_message_handler(equation_mentally_start, commands="equation_mentally")
    dp.register_message_handler(equation_mentally, state=Equation.equation_mentally)
    dp.register_message_handler(equation_mentally_answer, state=Equation.equation_mentally_answer)
