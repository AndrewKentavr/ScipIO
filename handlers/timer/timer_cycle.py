from datetime import datetime

from aiogram import types

from data_b.dp_control import get_cursor
from handlers.math.mentally_math import Equation


async def time_cycle(dp):
    cur = get_cursor()

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
