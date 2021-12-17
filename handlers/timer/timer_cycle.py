from datetime import datetime

from aiogram import types
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text
from aiogram.dispatcher import FSMContext

from data_b.dp_control import get_cursor
from handlers.flashcards.flashcards_training import Flash_game
from handlers.keyboards.default import flashcard_menu
from handlers.keyboards.inline import math_menu_inline
from handlers.math.mentally_math import Equation


async def time_cycle(dp):
    cur = get_cursor()

    now = datetime.now()
    time_now = now.strftime("%H:%M")

    cur.execute(f"""SELECT time, user_id, tasks FROM Time
                    where time == '{time_now}';""")
    time_results = cur.fetchall()
    if time_results:
        for i in time_results:
            user_id = i[1]
            tasks = i[2]
            # await dp.state.finish() # <-- Такое есть вообще???
            await dp.bot.send_message(user_id, 'Ежедневное задание',
                                      reply_markup=types.ReplyKeyboardRemove())

            # Дальше идёт проверка на то какие ежедневное задание какое типа выводить
            if tasks == 'Карточки (Flashcards)':
                await dp.bot.send_message(user_id, 'Ежедневное задание',
                                          reply_markup=types.ReplyKeyboardRemove())
                await dp.bot.send_message(user_id, 'Лайфхаки для работы с карточками /cards_info')
                await dp.bot.send_message(user_id, 'Вы готовы?',
                                          reply_markup=flashcard_menu.get_keyboard_flashcard_training_start())
                await Flash_game.fls_game.set()

            elif tasks == 'Математика в уме':
                await dp.bot.send_message(user_id, 'Чтобы вызвать подсказку напишите /mell_theory')
                await dp.bot.send_message(user_id, 'Вы готовы?', reply_markup=types.ReplyKeyboardRemove())
                await Equation.equation_mentally.set()

            elif tasks == 'Задачи по математике':
                await dp.bot.send_message(user_id, 'Выберете категорию заданий:',
                                          reply_markup=math_menu_inline.get_inline_math_problems_category())

            elif tasks == 'Задачи по логике':
                from handlers.keyboards.inline import logic_menu_inline
                await dp.bot.send_message(user_id, 'Выберете категорию заданий:',
                                          reply_markup=logic_menu_inline.get_inline_logic_problems_category())
