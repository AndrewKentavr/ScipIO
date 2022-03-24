from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji

from handlers.keyboards.default import math_menu


class MathButCategory(StatesGroup):
    """Данные state нужен, чтобы кнопки 'Задания из категорий' """
    math_category_step = State()


async def math_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Как работать: вы решаете задачу и сверяете свое решение или ответ с правильным, если сходится то нажимаете "Правильно" если нет то "Неправильно"')
    await message.answer('Выберите:', reply_markup=math_menu.get_keyboard_math_start())
    await MathButCategory.math_category_step.set()


def register_handlers_math(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='math', state="*")
