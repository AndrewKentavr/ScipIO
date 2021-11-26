from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_b.dp_control import flashcard_dp_create
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
        await message.answer(f'Вы превысили максимальное количество символов\n'
                             f'Повторите ещё раз')
        await FlashcardManaging.flashcards_managing_create_middle.set()
    else:
        await state.update_data(front=msg)

        await message.answer(f'Введите значение этой карточки\n'
                             f'Максимальное количество символов: <b>{MAX_LEN}</b>')
        await FlashcardManaging.next()


async def flashcards_managing_create_middle_2(message: types.Message, state: FSMContext):
    msg = message.text
    if len(msg) > MAX_LEN:
        await message.answer(f'Вы превысили максимальное количество символов\n'
                             f'Повторите ещё раз')
        await FlashcardManaging.flashcards_managing_create_middle_2.set()
    else:
        await state.update_data(back=msg)
        await message.answer(f'Вы хотите, чтобы при повторении карточки показывалась любая сторона?',
                             reply_markup=flashcard_menu.get_keyboard_flashcard_end_que())
        await FlashcardManaging.next()


async def flashcards_managing_create_end(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == 'Да' or msg == 'Нет':
        if msg == 'Да':
            show_card = True
        else:
            show_card = False
    else:
        await message.answer(f'Вы выбрали не то\n'
                             'Напишите "Да" или "Нет" или выберете кнопки в боте')
        await FlashcardManaging.flashcards_managing_create_end.set()

    user_data = await state.get_data()
    await message.answer('Создана карточка\n'
                         f'Передняя сторона - {user_data["front"]}')
    await message.answer(f'Задняя сторона - {user_data["back"]}')
    await message.answer(f'Показывать карточку с двух сторон? - {msg}')
    try:
        flashcard_dp_create(message.from_user.id, user_data["front"], user_data["back"], show_card)
        await message.answer(f'Всё успешно сохранилось')
    except Exception:
        await message.answer(f'Что - то пошло не так')
    await state.finish()


class FlashcardManaging(StatesGroup):
    flashcards_managing_create_middle = State()
    flashcards_managing_create_middle_2 = State()
    flashcards_managing_create_end = State()


def register_handlers_flashcards_managing(dp: Dispatcher):
    dp.register_message_handler(flashcards_managing_start, commands='flc_man', state='*')
    dp.register_message_handler(flashcards_managing_start, Text(equals="Управление карточками"), state='*')
    dp.register_message_handler(flashcards_managing_create_start, Text(equals="Создать карточку"), state='*')

    dp.register_message_handler(flashcards_managing_create_middle,
                                state=FlashcardManaging.flashcards_managing_create_middle)
    dp.register_message_handler(flashcards_managing_create_middle_2,
                                state=FlashcardManaging.flashcards_managing_create_middle_2)
    dp.register_message_handler(flashcards_managing_create_end,
                                state=FlashcardManaging.flashcards_managing_create_end)
