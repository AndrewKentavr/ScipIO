from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from dp.math_dp import timer_create_dp


async def timer_math_start(message: types.Message):
    await message.answer('Введите нужное вам время в формате:\n'
                         '<i>16:02</i>\n'
                         'Где <i>16</i> - это часы, а <i>02</i> - минуты', reply_markup=types.ReplyKeyboardRemove())
    await TimerMath.timer_math_create.set()


async def timer_math_create(message: types.Message, state: FSMContext):
    msg = message.text
    check_func = checking_message(msg)
    if isinstance(check_func, str):  # Проверка на то, что 'check_func' выводит ошибку, типа string
        await message.reply(check_func)
    else:
        timer_create_dp(message.from_user.id, msg)
        await message.reply('Время установлено')
        await state.finish()


async def timer_math_del(message: types.Message):
    pass


async def timer_math_info(message: types.Message):
    pass


class TimerMath(StatesGroup):
    timer_math_create = State()
    timer_math_del = State()
    timer_math_info = State()


def register_handlers_math_timer(dp: Dispatcher):
    dp.register_message_handler(timer_math_start, commands='timer_math', state="*")
    dp.register_message_handler(timer_math_start, Text(equals="Поставить таймер на отправку заданий", ignore_case=True),
                                state="*")
    dp.register_message_handler(timer_math_create, state=TimerMath.timer_math_create)
    dp.register_message_handler(timer_math_create, state=TimerMath.timer_math_del)
    dp.register_message_handler(timer_math_create, state=TimerMath.timer_math_info)


def checking_message(msg):
    """
    Проверка на то что число написанно вот так:
    16:02
    """

    if ':' in msg:
        c = msg.split(':')
        if len(c) == 2:
            try:
                int(c[0])
                int(c[1])
            except ValueError:
                return 'Введено не число'
            else:
                if len(c[1]) == 2:
                    if (0 <= int(c[0]) < 24) and (0 <= int(c[1]) < 60):
                        return True
                    else:
                        return 'Неправильное время'
                else:
                    return 'Введите числа, как показано в примере'
        else:
            return 'Переборщили со знаками'
    else:
        return 'Забыли про знак ":"'
