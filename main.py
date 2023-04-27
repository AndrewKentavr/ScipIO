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

from data_b.dp_control import dp_all_users_list, dp_all_telegram_id_flc_list, dp_user_create, \
    dp_all_telegram_id_time_list

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Логирование
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# создание обработчика для записи в файл
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

# создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# создание форматировщика логов
formatter = logging.Formatter(f'%(asctime)s - %(levelname)s ' + '- %(name)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# добавление обработчиков в логгер
logger.addHandler(file_handler)
logger.addHandler(console_handler)


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


async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
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
    scheduler.add_job(time_cycle, "interval", seconds=60, args=(dp,))
    scheduler.start()

    # Отключение логирования таймера
    logging.getLogger('apscheduler').setLevel(logging.WARNING)

    await set_commands(bot)

    # функция регистрации "register_message_handler"
    reg_cmd(dp)

    # Запуск полинга
    await dp.start_polling()


# Функция для оповещения ошибок
async def shutdown(error):
    user_id = ADMINS
    message = f"Ошибка: {error}"
    for i in user_id:
        await bot.send_message(chat_id=int(i), text=message)
        await bot.send_message(chat_id=int(i), text=message)
        await bot.send_message(chat_id=int(i), text=message)


if __name__ == "__main__":

    # ------------------------------------------------------
    """
        Это блок добавления пользователей в таблицу(users)
    
        Сделанн он, чтобы добавить всех пользователей в таблицу(users), у которых есть карточки flashcards и timer,
            т.к там хранится их 'telegram_user_id'
    """

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
    try:
        asyncio.run(main())
    except Exception as e:
        # логируем сообщение об ошибке
        logger.error(str(e))
        asyncio.run(shutdown(str(e)))
