from random import randint

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import ADMINS


async def cart_func(dp: Dispatcher):
    await dp.bot.send_message(ADMINS, 'ТАНЯ БЛЛЯЯЯЯЯЯЯЯ', reply_markup=types.ReplyKeyboardRemove())


async def ala_cart_func(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)


async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer(text="Спасибо, что воспользовались ботом!", show_alert=True)
    # или просто await call.answer()


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart_func, Text(equals=".-."), state="*")
    dp.register_message_handler(ala_cart_func, commands=['random'])
    dp.register_callback_query_handler(send_random_value, text="random_value")
