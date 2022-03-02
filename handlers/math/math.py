from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.keyboards.default import math_menu


class math_next_problem(StatesGroup):
    next_problem = State()


async def math_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите:', reply_markup=math_menu.get_keyboard_math_start())
    await math_next_problem.next_problem.set()


def register_handlers_math(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='math', state="*")
