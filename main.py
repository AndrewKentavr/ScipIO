from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.register_cmd import reg_cmd

from config import BOT_TOKEN, ADMINS
import logging

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    await set_commands(bot)
    reg_cmd(dp)  # функция регистрации "register_message_handler"
    await bot.send_message(ADMINS, "Bot - on", reply_markup=types.ReplyKeyboardRemove())


async def on_shutdown(dp):
    await bot.send_message(ADMINS, "Bot - Off", reply_markup=types.ReplyKeyboardRemove())
    # await bot.close()
    # await storage.close()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Просмотр функционала"),
        BotCommand(command="/math", description="Задания по математике"),
        BotCommand(command="/cancel", description="отмена действия")
    ]
    await bot.set_my_commands(commands)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
