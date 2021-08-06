from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from asyncio import sleep as async_sleep

from handlers.math.mentally_math import Equation


async def timer_math_start(message: types.Message):
    await message.answer('Введите нужное вам время в формате:\n'
                         '<i>16_02</i>\n'
                         'Где <i>16</i> - это часы, а <i>02</i> - минуты', reply_markup=types.ReplyKeyboardRemove())
    await TimerMath.timer_math.set()


async def timer_math(message: types.Message):
    time_msg = message.text.split('_')
    hour, min = int(time_msg[0]), int(time_msg[1])
    await message.reply('Время установлено')

    """Есть идея засунуть while true прям сюда, но я ещё не уверен"""

    while True:
        await async_sleep(60)
        now = datetime.now()
        if now.hour == hour and now.minute == min:
            await message.answer('Ежедневное задание')
            await message.answer('Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
            await Equation.equation_mentally.set()


class TimerMath(StatesGroup):
    timer_math = State()


def register_handlers_math_timer(dp: Dispatcher):
    dp.register_message_handler(timer_math_start, commands='timer_math', state="*")
    dp.register_message_handler(timer_math_start, Text(equals="Поставить таймер на отправку заданий", ignore_case=True),
                                state="*")
    dp.register_message_handler(timer_math, state=TimerMath.timer_math)
