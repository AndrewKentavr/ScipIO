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
    photo = InputFile("data/math_1.jpg")
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

    photo_2 = InputFile("data/math_2.jpg")
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
    await message.answer('Вы готовы?', reply_markup=math_menu.get_keyboard_math_mentally_start())
    await Equation.equation_mentally_beginning.set()


async def equation_mentally_beginning(message: types.Message, state: FSMContext):
    if message.text != 'Да':
        await message.answer('Вы написали что-то не то')
        return
    else:

        # Генерирует пример ввида [equation, answer]
        equation = equation_generate()

        # ------  Создание user_data ---------

        # В начале программы 'user_data' - пуста и создаются сделующие списки
        await state.update_data(condition=[])
        await state.update_data(answer=[])
        await state.update_data(attempts=[])

        user_data = await state.get_data()

        # ------  Определение user_data -------
        # хранит все условия примеров
        conditions = user_data['condition']
        conditions.append(equation[0])
        await state.update_data(condition=conditions)

        # хранит все ответы примеров
        answers = user_data['answer']
        answers.append(equation[1])
        await state.update_data(answer=answers)

        # хранит всё количество попыток на ответы примеров
        attempt = user_data['attempts']
        # Количество попыток мы создаём 0 - это сделанно для того, чтобы если пользователь завершит задание, не
        # приступив к нему, то это не покажется в статистике, т.к попыток НОЛЬ
        attempt.append(0)
        await state.update_data(attempts=attempt)

        await message.answer(f'Решите в уме:\n{equation[0]}')
        await Equation.equation_mentally.set()


async def equation_mentally(message: types.Message, state: FSMContext):
    try:
        msg = int(message.text)
    except ValueError:
        await message.answer(f'Неправильные знаки')
    else:
        user_data = await state.get_data()

        answers = user_data['answer']
        conditions = user_data['condition']
        attempts = user_data['attempts']

        # считает количество попыток и прибавляет
        cc = int(attempts[-1]) + 1
        attempts[-1] = cc
        await state.update_data(attempts=attempts)

        if msg != int(answers[-1]):

            await message.answer('Неправильно, попробуйте ещё раз')
            if int(attempts[-1]) % 3 == 0:
                await message.answer('Посмотрите ещё раз "подсказку":\n'
                                     'Для этого нажмите или наберите /mell_theory')
            await message.answer(f'Решите в уме:\n{conditions[-1]}')
            return
        else:
            await message.answer('Правильно, следующее задание')

            # Генерирует пример ввида [equation, answer]
            equation = equation_generate()

            # ------  Добавляем примеры, ответы, попытки в  user_data -------

            conditions.append(equation[0])
            await state.update_data(condition=conditions)
            answers.append(equation[1])
            await state.update_data(answer=answers)
            # Количество попыток мы создаём 0 - это сделанно для того, чтобы если пользователь завершит задание, не
            # приступив к нему, то это не покажется в статистике, т.к попыток НОЛЬ
            attempts.append(0)
            await state.update_data(attempts=attempts)

            await message.answer(f'Решите в уме:\n{equation[0]}')

            await Equation.equation_mentally.set()


class Equation(StatesGroup):
    equation_mentally_beginning = State()
    equation_mentally = State()


def equation_generate():
    """
    Функция создаёт математический пример состоящий из 2'х значных чисел и
    перемножет их или возводит в степень

    :return: equation - Математический пример
    :return: answer - Ответ на пример
    """
    mathematically_signs = ['*', '**']
    sign = choice(mathematically_signs)
    A = str(randint(11, 99))
    if sign == '**':
        B = 2
    else:
        B = str(randint(11, 99))
    equation = f'{A} {sign} {B}'
    answer = eval(equation)
    print(answer)

    return [equation, answer]


def register_handlers_math_mentally(dp: Dispatcher):
    dp.register_message_handler(equation_mentally_theory, commands='mell_theory', state='*')

    dp.register_message_handler(equation_mentally_start, Text(equals="Примеры для подсчёта в уме"))
    dp.register_message_handler(equation_mentally_start, commands="equation_mentally")
    dp.register_message_handler(equation_mentally_beginning, state=Equation.equation_mentally_beginning)
    dp.register_message_handler(equation_mentally, state=Equation.equation_mentally)
