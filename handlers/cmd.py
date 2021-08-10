from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher import FSMContext

from config import ADMINS
from handlers.timer.check_timer import timer_cycle

dp_main = 0


async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = ["/math", ]
    keyboard.add(*button_1)
    await message.answer(f'Привет, {message.from_user.full_name}! '
                         f'Посмотри на это:', reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def cmd_timer_start(message: types.Message):
    await message.answer("Таймер начался", reply_markup=types.ReplyKeyboardRemove())
    await timer_cycle(dp_main)


def register_handlers_start(dp: Dispatcher):
    global dp_main
    dp_main = dp
    dp.register_message_handler(cmd_start, CommandStart(), state='*')
    dp.register_message_handler(cmd_start, CommandHelp(), state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_timer_start, IDFilter(user_id=ADMINS), commands='start_timers')
