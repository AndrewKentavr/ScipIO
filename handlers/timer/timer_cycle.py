"""
    Алгоритм таймера работает следующим образом:
    Раз в 60 секунд запускается проверка, есть ли данное время (например 16:03) в базе данных time
        и если есть то выводит "Ежедневное задание"
"""

from aiogram import types
from data_b.dp_control import dp_timer_circle_user_time, del_user
from handlers.flashcards.flashcards_training import Flash_game
from handlers.keyboards.default import flashcard_menu, math_menu
from handlers.keyboards.inline import math_menu_inline
from handlers.math.mentally_math import Equation
import pytz
from datetime import datetime


async def time_cycle(dp):
    # Определение времени по московскому времени (небходимо для сервера, чтобы он определял какое время сейчас в Москве)
    time_moscow = datetime.now(pytz.timezone('Europe/Moscow'))
    time_now = time_moscow.strftime("%H:%M")

    # Массив telegram_user_id и tasks, таймер которых совпал с нужным временем
    time_results = dp_timer_circle_user_time(time_now)

    if time_results:
        for i in time_results:
            user_id = i[0]
            tasks = i[1]
            """
            Без создания state, на версии 2.16 aiogram выдаёт ошибку:
                AttributeError: 'NoneType' object has no attribute 'current_state'
                Поэтому надо создавать state вручную
            """
            state = dp.current_state(chat=user_id, user=user_id)

            await dp.bot.send_message(user_id, 'Ежедневное задание!',
                                      reply_markup=types.ReplyKeyboardRemove())

            # Идёт проверка какого типо tasks
            if tasks == 'Карточки (Flashcards)':
                await dp.bot.send_message(user_id, 'Лайфхаки для работы с карточками /cards_info')
                await dp.bot.send_message(user_id, 'Вы готовы?',
                                          reply_markup=flashcard_menu.get_keyboard_flashcard_training_start())
                await state.set_state(Flash_game.flc_game)

            elif tasks == 'Математика в уме':
                await dp.bot.send_message(user_id, 'Чтобы вызвать подсказку напишите /mell_theory')
                await dp.bot.send_message(user_id, 'Вы готовы?',
                                          reply_markup=math_menu.get_keyboard_math_mentally_start())
                await state.set_state(Equation.equation_mentally_beginning)

            elif tasks == 'Задачи по математике':
                await dp.bot.send_message(user_id, 'Выберете категорию заданий:',
                                          reply_markup=math_menu_inline.get_inline_math_problems_category())

            elif tasks == 'Задачи по логике':
                from handlers.keyboards.inline import logic_menu_inline
                await dp.bot.send_message(user_id, 'Выберете категорию заданий:',
                                          reply_markup=logic_menu_inline.get_inline_logic_problems_category())
