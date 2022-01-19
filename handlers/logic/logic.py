from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.keyboards.default import logic_menu


async def math_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите:', reply_markup=logic_menu.get_keyboard_logic_start())


def register_handlers_logic(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='logic', state="*")
