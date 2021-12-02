from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.keyboards.default import flashcard_menu


async def flashcards_training_start(message: types.Message):
    await message.answer('Лайфхаки для работы с карточками /cards_info')
    await message.answer('Вы готовы?', reply_markup=flashcard_menu.get_keyboard_flashcard_training_start())


async def fls_game_start(message: types.Message, state: FSMContext):
    pass


def flashcard_generate(user_id):
    pass


def register_handlers_flashcards_training(dp: Dispatcher):
    dp.register_message_handler(flashcards_training_start, commands='flc_train', state='*')
    dp.register_message_handler(flashcards_training_start, Text(equals="Начать учить карточки"), state='*')
