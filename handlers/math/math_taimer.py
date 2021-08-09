from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from asyncio import sleep as async_sleep

from handlers.math.mentally_math import Equation
from dp.math_dp import timer_create_dp


async def timer_math_start(message: types.Message):
    await message.answer('Введите нужное вам время в формате:\n'
                         '<i>16_02</i>\n'
                         'Где <i>16</i> - это часы, а <i>02</i> - минуты', reply_markup=types.ReplyKeyboardRemove())
    await TimerMath.timer_math_create.set()


async def timer_math_create(message: types.Message):
    msg = message.text
    await message.reply('Время установлено')
    timer_create_dp(message.from_user.id, msg)
    await message.answer('ЗАЕБИСЬ ЗАЕБИСЬ ЗАЕБИСЬ ЗАЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕБИСЬ')

    """Есть идея засунуть while true прям сюда, но я ещё не уверен"""


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
