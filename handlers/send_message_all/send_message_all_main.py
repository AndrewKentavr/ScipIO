from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from handlers.send_message_all.send_message_all import send_message_all
from config import ADMINS
from handlers.keyboards.default.send_message_all import main_send_msg


async def send_msg_start_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Отправка сообщения всем\nВведите сообщение', reply_markup=main_send_msg())


def register_handlers_send_msg(dp: Dispatcher):
    dp.register_message_handler(send_msg_start_main, IDFilter(user_id=ADMINS), commands='message', state="*")
    dp.register_message_handler(send_msg_start_main, Text(equals="Нет"), IDFilter(user_id=ADMINS),
                                state=send_message_all.main_message3)
