from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from dp.math_dp import timer_create_dp, timer_info_dp, timer_del_dp
from handlers.keyboards.default import math_menu


async def timer_math_select(message: types.Message):
    await message.answer('Выберете:', reply_markup=math_menu.get_keyboard_math_timer())


async def timer_math_create_start(message: types.Message):
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
        await message.reply('Таймер установлен')
        await state.finish()


async def timer_math_del_start(message: types.Message):
    user_id = message.from_user.id
    await message.answer('Удалите таймер, написав время таймера сюда\n'
                         'Вот так: <i>16:02</i>', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Какой из таймеров вы хотите удалить?')
    all_timers = timer_info_dp(user_id)
    for i in all_timers:
        await message.answer(f'{i}')
    await TimerMath.timer_math_del.set()


async def timer_math_del(message: types.Message, state: FSMContext):
    msg = message.text
    check_func = checking_message(msg)
    if isinstance(check_func, str):  # Проверка на то, что 'check_func' выводит ошибку, типа string
        await message.reply(check_func)
    else:
        timer_del_dp(message.from_user.id, msg)
        await message.reply('Таймер удалён')
        await state.finish()


async def timer_math_info(message: types.Message):
    user_id = message.from_user.id
    await message.answer('Вот все ваши таймеры:', reply_markup=types.ReplyKeyboardRemove())
    all_timers = timer_info_dp(user_id)
    for i in all_timers:
        await message.answer(f'{i}')


class TimerMath(StatesGroup):
    timer_math_create = State()
    timer_math_del = State()


def register_handlers_math_timer(dp: Dispatcher):
    dp.register_message_handler(timer_math_select, commands='timer_math', state="*")
    dp.register_message_handler(timer_math_select, Text(equals="Математический таймер", ignore_case=True),
                                state="*")

    dp.register_message_handler(timer_math_create_start, Text(equals="Создать таймер", ignore_case=True))
    dp.register_message_handler(timer_math_del_start, Text(equals="Удалить таймер", ignore_case=True))
    dp.register_message_handler(timer_math_info, Text(equals="Посмотреть все таймеры", ignore_case=True))

    dp.register_message_handler(timer_math_create, state=TimerMath.timer_math_create)
    dp.register_message_handler(timer_math_del, state=TimerMath.timer_math_del)


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
