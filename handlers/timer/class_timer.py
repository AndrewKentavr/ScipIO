from asyncio import sleep as async_sleep
from datetime import datetime

from aiogram import types
from aiogram.types import message

from config import ADMINS
from handlers.math.mentally_math import Equation

ALL_TIMERS = {}


class Timer:
    def __init__(self, Dispatcher, hour, min, user_id):
        self.hour = hour
        self.min = min
        self.check = True
        self.dp = Dispatcher
        self.user_id = user_id

    async def wait_timer_func(self):
        while self.check:
            await async_sleep(60)
            now = datetime.now()
            if now.hour == self.hour and now.minute == self.min:
                await self.dp.bot.send_message(self.user_id, 'Ежедневное задание', reply_markup=types.ReplyKeyboardRemove())
                await self.dp.bot.send_message(self.user_id, 'Вы готовы?')
                await Equation.equation_mentally.set()
