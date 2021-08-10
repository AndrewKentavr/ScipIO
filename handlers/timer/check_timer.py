import sqlite3
from asyncio import sleep as async_sleep
from datetime import datetime

from aiogram import types

from handlers.math.mentally_math import Equation

"""
Создать только один цикл await async_sleep(60)
и потом проверять у пользователя наличие данного таймера
--------
Создать 1 цикл await async_sleep(60)
который будет просто в данное время присылать определённым пользователем сообщение
"""


async def timer_cycle(dp):
    while True:
        await async_sleep(30)
        CONN = sqlite3.connect('C:/Users/andrt/PycharmProjects/ConTia/dp/contia_dp.db')
        cur = CONN.cursor()

        now = datetime.now()
        time_now = now.strftime("%H:%M")

        cur.execute(f"""SELECT time, user_id FROM Time
                        where time == '{time_now}';""")
        time_results = cur.fetchall()
        if time_results:
            for i in time_results:
                user_id = i[1]
                await dp.bot.send_message(user_id, 'Ежедневное задание',
                                          reply_markup=types.ReplyKeyboardRemove())
                await dp.bot.send_message(user_id, 'Вы готовы?')
                await Equation.equation_mentally.set()
