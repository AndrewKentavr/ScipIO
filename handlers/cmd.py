import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message):
    await message.answer(f'Приветствуем на нашем обучающем проекте!' + emoji.emojize(":fire:"))
    await message.answer(
        f'Мы создали его для людей которые хотят развить свои навыки или получить новые.' + emoji.emojize(":brain:"))
    await message.answer(f'В функционал проекта входят:'
                         f'\n 1) Математические задачи'
                         f'\n 2) Математические примеры в уме'
                         f'\n 3) Задачи на логику (данетки, загадки, логические задачи)'
                         f'\n 4) Карточки для запоминания'
                         f'\n 5) Таймер')
    await message.answer(f'Это только первая версия, в дальнейшем она будет улучшаться и функционал будет расширяться.')
    await message.answer(f'Команды для взаимодействия с ботом:'
                         f'\n 1) /math - Задачи по математике'
                         f'\n 2) /logic - Задачи на логику'
                         f'\n 3) /flashcard - Карточки для запоминания'
                         f'\n 4) /timer - Таймер'
                         f'\n 5) /help - Просмотр функционала'
                         f'\n 6) /cancel - Отмена действия')


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
