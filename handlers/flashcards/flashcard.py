from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.keyboards.default import flashcard_menu


async def flashcard_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('"Начать учить карточки" - начнёт  процесс тренировки с карточками')
    await message.answer('"Управление карточками" - переправит в раздел для изменения карточек',
                         reply_markup=flashcard_menu.get_keyboard_flashcard_start())


def register_handlers_flashcard(dp: Dispatcher):
    dp.register_message_handler(flashcard_start, commands='flashcard', state="*")
