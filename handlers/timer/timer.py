from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from handlers.keyboards.default import timer_menu


async def timer_select(message: types.Message):
    await message.answer('Выберете:', reply_markup=timer_menu.get_keyboard_timer())


def register_handlers_timer(dp: Dispatcher):
    dp.register_message_handler(timer_select, commands='timer', state="*")
    dp.register_message_handler(timer_select, Text(equals="Таймер", ignore_case=True),
                                state="*")