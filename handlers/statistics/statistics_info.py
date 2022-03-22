from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import emoji
from data_b.dp_control import stat_general_bd, stat_bar_general
from handlers.statistics.charts import pie_chart, bar_chart
from aiogram.types import InputFile
import os


# ---------------------------general (общая статистика)------------------------------
async def stat_general(message: types.Message):
    user_id = message.from_user.id
    info_general = stat_general_bd(user_id)[0]
    await message.answer(f'Ваша общая статистика:\n'
                         f'Показов flashcard: {info_general[0]}\n'
                         f'Попыток mentally math: {info_general[1]}\n'
                         f'Показов category_math: {info_general[2]}\n'
                         f'Показов category_logic: {info_general[3]}', reply_markup=types.ReplyKeyboardRemove())

    pie_chart(info_general, user_id)
    photo = InputFile(f"handlers/statistics/data_figure/{user_id}.png")
    await message.answer_photo(photo=photo)
    os.remove(f"handlers/statistics/{user_id}.png")

    list_time = stat_bar_general(user_id)
    bar_chart(list_time, user_id)
    photo = InputFile(f"handlers/statistics/data_figure/{user_id}.png")
    await message.answer_photo(photo=photo)
    os.remove(f"handlers/statistics/{user_id}.png")

    return


def register_handlers_statistics_info(dp: Dispatcher):
    dp.register_message_handler(stat_general,
                                Text(equals=emoji.emojize(":bar_chart:") + ' Общая'), state='*')
