from random import randint

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import ADMINS


# async def cart_func_admin(dp: Dispatcher):
#     await dp.bot.send_message(ADMINS, 'ТАНЯ БЛЛЯЯЯЯЯЯЯЯ', reply_markup=types.ReplyKeyboardRemove())


async def cart_func(message: types.Message):
    await message.answer(
        'Котик, я выпустил этот проект, и я хочу, чтобы ты знала, что я очень тебя люблю.\n'
        'Сейчас время 10:58 20.01.2022. И я хочу сказать, что если бы не ты, этого проекта скорее всего не было бы,'
        ' потому что'
        'только ты заставляла вставать в 5 утра и делать проект. Мне очень тяжело без тебя, я просто хочу быть с тобой',
        reply_markup=types.ReplyKeyboardRemove())

    await message.answer('<3..')


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart_func, Text(equals=".-."), state="*")
