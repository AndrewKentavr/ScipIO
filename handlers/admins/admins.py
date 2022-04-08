from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from config import ADMINS
from handlers.keyboards.default.admin_menu import admin_start_menu


async def admin_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберете:', reply_markup=admin_start_menu())


def register_handlers_send_msg(dp: Dispatcher):
    dp.register_message_handler(admin_start, IDFilter(user_id=ADMINS), commands='admin', state="*")
