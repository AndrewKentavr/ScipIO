from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp


async def bot_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = ["/math", ]
    keyboard.add(*button_1)
    await message.answer(f'Привет, {message.from_user.full_name}! '
                         f'Посмотри на это:', reply_markup=keyboard)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_start, CommandHelp())
