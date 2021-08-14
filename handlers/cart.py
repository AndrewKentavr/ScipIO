from random import randint

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import ADMINS


async def cart_func(dp: Dispatcher):
    await dp.bot.send_message(ADMINS, 'ТАНЯ БЛЛЯЯЯЯЯЯЯЯ', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart_func, Text(equals=".-."), state="*")
