"""
Присылает администраторам бота информацию:
    1. Количество пользователй за всё время
    2. Количество новых пользователей за день
    3. Количество новых пользователей за последние 7 дней
    4. Количество новых пользователей за последние 30 дней

"""

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import IDFilter, Text

from config import ADMINS
from data_b.dp_control import dp_admin_stat
import datetime
import pytz


def users_new(users_list, time):
    """
    Подсчёт новый пользователй за определённое время
    :param users_list: массив время регистрации пользователей
    :param time: нужное время
    :return: количество новый пользователей
    """
    time_moscow = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    arr_time_week = [(time_moscow - datetime.timedelta(days=time - 1 - i)).strftime("%Y-%m-%d") for i in range(time)]

    count = 0
    for i in users_list:
        if i[1][0:10] in arr_time_week:
            count += 1

    return count


async def stat_admins(message: types.Message):
    all_users_list = dp_admin_stat()
    users_today = users_new(all_users_list, 1)
    users_week = users_new(all_users_list, 7)

    # Новых пользователей за последние 30 дней
    users_month = users_new(all_users_list, 30)

    await message.answer(f'Всего пользователей: {len(all_users_list)}\n'
                         f'Новых за день: {users_today}\n'
                         f'Новых за неделю: {users_week}\n'
                         f'Новых за месяц: {users_month}\n', reply_markup=types.ReplyKeyboardRemove())
    return


def register_handlers_statistics_info_admins(dp: Dispatcher):
    dp.register_message_handler(stat_admins, IDFilter(user_id=ADMINS), Text(equals='Статистика пользователей'),
                                state="*")
