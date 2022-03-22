import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

import middlewares
from config import BOT_TOKEN, ADMINS
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.timer.timer_cycle import time_cycle
from handlers.register_cmd import reg_cmd

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/cancel", description="Отмена действия"),
        BotCommand(command="/help", description="Просмотр функционала"),
        BotCommand(command="/math", description="Задания по математике"),
        BotCommand(command="/logic", description="Задания по логике"),
        BotCommand(command="/flashcard", description="Карточки для запомнинания"),
        BotCommand(command="/statistics", description="Просмотр статистики"),
        BotCommand(command="/timer", description="Таймер")
    ]
    await bot.set_my_commands(commands)


def timer_interval_func():
    """
    Запускает функцию time_cycle, каждые 60 секунд
    """
    scheduler.add_job(time_cycle, "interval", seconds=60, args=(dp,))


async def main():
    """
    await bot.delete_webhook(drop_pending_updates=True) - в новых версиях aiogram есть проблема, то что при запуске бота,
        он реагирует на сообщения, которые были отправленны ему, пока он был выключен и это не чинилось dp.skip_updates()
        подробнее об этой ошибке: https://github.com/aiogram/aiogram/issues/418
    """
    # Удаление последнего сообщения
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск "антифлуда"
    middlewares.setup(dp)

    # Это запуск таймера AsyncIOScheduler
    scheduler.start()
    # Запуск функции таймера
    timer_interval_func()

    await set_commands(bot)

    # функция регистрации "register_message_handler"
    reg_cmd(dp)

    # Запуск полинга
    await dp.start_polling()


if __name__ == "__main__":

    # ------------------------------------------------------
    """
        Это блок добавления пользователей в таблицу(users)
    
        Сделанн он, чтобы добавить всех пользователей в таблицу(users), у которых есть карточки flashcards и timer,
            т.к там хранится их 'telegram_user_id'
    """

    from data_b.dp_control import dp_all_users_list, dp_all_telegram_id_flc_list, dp_user_create, \
        dp_all_telegram_id_time_list

    all_users_list = dp_all_users_list()
    all_telegram_id_flc = dp_all_telegram_id_flc_list()

    for i in all_telegram_id_flc:
        if i not in all_users_list:
            dp_user_create(i)

    all_telegram_id_time = dp_all_telegram_id_time_list()

    for i in all_telegram_id_time:
        if i not in all_users_list:
            dp_user_create(i)
    # ------------------------------------------------------

    # Ассинхронный запуск бота
    asyncio.run(main())
