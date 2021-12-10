import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.register_cmd import reg_cmd

from config import BOT_TOKEN, ADMINS
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.timer.check_timer import time_check

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
scheduler = AsyncIOScheduler()


# async def on_startup(dp):
#     await set_commands(bot)
#     reg_cmd(dp)  # функция регистрации "register_message_handler"
#     await bot.send_message(ADMINS, "Bot - on", reply_markup=types.ReplyKeyboardRemove())
#
#
# async def on_shutdown(dp):
#     await bot.send_message(ADMINS, "Bot - Off", reply_markup=types.ReplyKeyboardRemove())
#     # await bot.close()
#     # await storage.close()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Просмотр функционала"),
        BotCommand(command="/math", description="Задания по математике"),
        BotCommand(command="/logic", description="Задания по логике"),
        BotCommand(command="/flashcard", description="Карточки для запомнинания"),
        BotCommand(command="/cancel", description="Отмена действия")
    ]
    await bot.set_my_commands(commands)


def timer_interval_func():
    """
    Функция управляющая таймером
    """
    scheduler.add_job(time_check, "interval", seconds=60, args=(dp,))


async def main():
    """
    scheduler.start(), check_func() - запуск таймера и функция работающая с ним
    set_commands - назначает комманды бота
    reg_cmd - регистрация фсех необходимых функция

    """

    scheduler.start()
    timer_interval_func()

    await set_commands(bot)
    reg_cmd(dp)  # функция регистрации "register_message_handler"
    await bot.send_message(ADMINS, "Bot - on", reply_markup=types.ReplyKeyboardRemove())

    # Запуск поллинга
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
