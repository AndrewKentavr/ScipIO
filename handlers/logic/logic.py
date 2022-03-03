from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.keyboards.default import logic_menu


class logic_next_problem(StatesGroup):
    next_problem = State()


async def math_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите:', reply_markup=logic_menu.get_keyboard_logic_start())
    await logic_next_problem.next_problem.set()


def register_handlers_logic(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='logic', state="*")
