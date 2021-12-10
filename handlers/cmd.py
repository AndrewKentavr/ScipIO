from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = ["/math", ]
    keyboard.add(*button_1)
    await message.answer(f'Привет, {message.from_user.full_name}! '
                         f'Посмотри на это:', reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_start(dp: Dispatcher):
    global dp_main
    dp_main = dp
    dp.register_message_handler(cmd_start, CommandStart(), state='*')
    dp.register_message_handler(cmd_start, CommandHelp(), state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
