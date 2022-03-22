from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.keyboards.default import statistics_menu


async def stat_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите:', reply_markup=statistics_menu.get_keyboard_statistics_start())


def register_handlers_statistics(dp: Dispatcher):
    dp.register_message_handler(stat_start, commands='statistics', state="*")
