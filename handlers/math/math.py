from aiogram import types, Dispatcher


from handlers.keyboards.default import math_menu


async def math_start(message: types.Message):
    await message.answer('Выберите:', reply_markup=math_menu.get_keyboard_math_start())


def register_handlers_math(dp: Dispatcher):
    dp.register_message_handler(math_start, commands='math', state="*")
