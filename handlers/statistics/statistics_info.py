from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import emoji
from data_b.dp_control import stat_general_bd


# ---------------------------general (общая статистика)------------------------------
async def stat_general(message: types.Message):
    info_general = stat_general_bd(message.from_user.id)[0]

    await message.answer(f'Ваша общая статистика:\n'
                         f'Показов flashcard: {info_general[0]}\n'
                         f'Попыток mentally math: {info_general[1]}\n'
                         f'Показов category_math: {info_general[2]}\n'
                         f'Показов category_logic: {info_general[3]}', reply_markup=types.ReplyKeyboardRemove())
    return


def register_handlers_statistics_info(dp: Dispatcher):
    dp.register_message_handler(stat_general,
                                Text(equals=emoji.emojize(":bar_chart:") + ' Общая'), state='*')
