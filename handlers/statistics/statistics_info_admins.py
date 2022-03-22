from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import IDFilter

from config import ADMINS
from data_b.dp_control import dp_admin_stat
import datetime
import pytz


def users_new(users_list, time):
    users_new_today_list = []
    time_moscow = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    arr_time_week = [(time_moscow - datetime.timedelta(days=time - 1 - i)).strftime("%Y-%m-%d") for i in range(time)]

    for i in users_list:
        if i[1][0:10] in arr_time_week:
            users_new_today_list.append(i[0])

    return users_new_today_list


async def stat_admins(message: types.Message):
    all_users_list = dp_admin_stat()
    users_today = users_new(all_users_list, 1)
    users_week = users_new(all_users_list, 7)

    # Новых пользователей за последние 30 дней
    users_month = users_new(all_users_list, 30)

    await message.answer(f'Всего пользователей: {len(all_users_list)}\n'
                         f'Новых за день: {len(users_today)}\n'
                         f'Новых за неделю: {len(users_week)}\n'
                         f'Новых за месяц: {len(users_month)}\n')
    return


def register_handlers_statistics_info_admins(dp: Dispatcher):
    dp.register_message_handler(stat_admins, IDFilter(user_id=ADMINS), commands='admin_stat', state="*")
