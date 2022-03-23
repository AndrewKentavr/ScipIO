from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from config import ADMINS
from handlers.keyboards.default.admin_menu import main_send_msg


async def send_msg_start_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберете:', reply_markup=main_send_msg())


def register_handlers_send_msg(dp: Dispatcher):
    dp.register_message_handler(send_msg_start_main, IDFilter(user_id=ADMINS), commands='admin', state="*")
