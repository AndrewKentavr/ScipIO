import asyncio
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.register_cmd import reg_cmd

from config import BOT_TOKEN, ADMINS
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from handlers.timer.check_timer import timer_cycle

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


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
        BotCommand(command="/cancel", description="Отмена действия")
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Создаём бота
    set_commands - назначает комманды бота
    reg_cmd - регистрация фсех необходимых функция

    """
    # Настройка логирования в stdout
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)

    await set_commands(bot)
    reg_cmd(dp)  # функция регистрации "register_message_handler"
    await bot.send_message(ADMINS, "Bot - on", reply_markup=types.ReplyKeyboardRemove())

    # Запуск поллинга
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":

    # scheduler = BackgroundScheduler()
    # scheduler.add_executor('processpool')
    # scheduler.add_job(timer_cycle, 'interval', seconds=3)
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    #
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass


    asyncio.run(main())
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
