from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import emoji


# ---------------------------general (общая статистика)------------------------------
async def stat_general(message: types.Message):
    await message.answer('Ваша общая статистика:', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_statistics_info(dp: Dispatcher):
    dp.register_message_handler(stat_general,
                                Text(equals=emoji.emojize(":bar_chart:") + ' Общая'), state='*')
