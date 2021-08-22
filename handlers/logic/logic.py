from aiogram import types, Dispatcher


from handlers.keyboards.default import logic_menu


async def math_start(message: types.Message):
    await message.answer('Выберете:', reply_markup=logic_menu.get_keyboard_logic_start())


def register_handlers_math(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='logic', state="*")
