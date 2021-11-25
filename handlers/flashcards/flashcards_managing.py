from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.keyboards.default import flashcard_menu

MAX_LEN = 450


async def flashcards_managing_start(message: types.Message):
    await message.answer('Выберете, что вы хотите делать с flashcards ',
                         reply_markup=flashcard_menu.get_keyboard_flashcard_managing())


async def flashcards_managing_create_start(message: types.Message):
    await message.answer(f'Введите нужную вам карточку\n'
                         f'Максимальное количество символов: <b>{MAX_LEN}</b>',
                         reply_markup=types.ReplyKeyboardRemove())
    await FlashcardManaging.flashcards_managing_create_middle.set()


async def flashcards_managing_create_middle(message: types.Message, state: FSMContext):
    msg = message.text
    if len(msg) > MAX_LEN:
        await message.answer(f'Вы превысили максимальное количество символов'
                             f'Повторите ещё раз')
        await FlashcardManaging.flashcards_managing_create_middle.set()
    else:
        await state.update_data(front=msg)

        await message.answer(f'Введите значение этой карточки\n'
                             f'Максимальное количество символов: <b>{MAX_LEN}</b>')


async def flashcards_managing_create_middle(message: types.Message, state: FSMContext):
    msg = message.text
    if len(msg) > MAX_LEN:
        await message.answer(f'Вы превысили максимальное количество символов'
                             f'Повторите ещё раз')
        await FlashcardManaging.flashcards_managing_create_middle.set()
    else:
        await state.update_data(front=msg)

        await message.answer(f'Введите значение этой карточки\n'
                             f'Максимальное количество символов: <b>{MAX_LEN}</b>')


# async def flashcards_managing_start(message: types.Message):
#     await message.answer('Выберете, что вы хотите делать с flashcards ',
#                          reply_markup=flashcard_menu.get_keyboard_flashcard_managing())
#
#
# async def flashcards_managing_start(message: types.Message):
#     await message.answer('Выберете, что вы хотите делать с flashcards ',
#                          reply_markup=flashcard_menu.get_keyboard_flashcard_managing())

class FlashcardManaging(StatesGroup):
    flashcards_managing_create_middle = State()
    flashcards_managing_create_end = State()


def register_handlers_math_mentally(dp: Dispatcher):
    dp.register_message_handler(flashcards_managing_start, commands='flc_man', state='*')
    dp.register_message_handler(flashcards_managing_start, Text(equals="Управление карточками"))

    dp.register_message_handler(flashcards_managing_create_middle,
                                state=FlashcardManaging.flashcards_managing_create_middle)
    dp.register_message_handler(flashcards_managing_create_middle,
                                state=FlashcardManaging.flashcards_managing_create_middle)
