from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji

from data_b.dp_control import flashcard_dp_create, flashcard_dp_info, flashcard_del_check, flashcard_del
from handlers.keyboards.default import flashcard_menu

MAX_LEN = 450


async def flashcards_managing_start(message: types.Message):
    await message.answer('Вы можете создать или удалить собственные карточки, а также просмотреть информацию о них',
                         reply_markup=flashcard_menu.get_keyboard_flashcard_managing())


# -----------------------------CREATE FUNC-----------------------------------------


async def flashcards_managing_create_start(message: types.Message):
    await message.answer(f'Введите слово или фразу, которое/ую хотите выучить\n'
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

        await message.answer(f'Введите значение или перевод первой стороны карточки\n'
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
        await message.answer(f'Карточка успешно сохранена', reply_markup=types.ReplyKeyboardRemove())
    except Exception:
        await message.answer(f'Что - то пошло не так')
    await state.finish()


# -----------------------------DEL FUNC-----------------------------------------
async def flashcards_managing_del_start(message: types.Message):
    all_cards = flashcard_dp_info(message.from_user.id)
    if len(all_cards) == 0:
        await message.answer(f'У вас нет карточек, которые вы могли бы удалалять',
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f'Сначала создайте их')
        return

    await message.answer(f'Чтобы удалить карточку - введите её id',
                         reply_markup=types.ReplyKeyboardRemove())
    mes_print = 'id     :     front     :      back\n'
    for i in all_cards:
        mes_print += f'{i[0]}: {i[1]} - {i[2]}\n'

    await message.answer(mes_print)
    await FlashcardManaging.flashcards_managing_del_end.set()


async def flashcards_managing_del_end(message: types.Message, state: FSMContext):
    msg = message.text
    list_id = msg.split(', ')
    for card_id in list_id:
        if card_id.isdigit():
            if flashcard_del_check(card_id):
                flashcard_del(card_id)
                await message.reply(f'Карточка - {card_id} успешно удалена')
                await state.finish()

            else:
                await message.answer('Такого id карточки - не существует')
                await FlashcardManaging.flashcards_managing_del_end.set()
        else:
            await message.answer('Вы неправильно ввели id карточки\n'
                                 'Напишите как показано в примере:\n'
                                 'Если карточка одна: 3242\n'
                                 'Если карточек несколько: 3242, 3346, 7285\n')
            await FlashcardManaging.flashcards_managing_del_end.set()


async def flashcards_managing_info(message: types.Message):
    await message.answer('Все ваши карточки:', reply_markup=types.ReplyKeyboardRemove())
    all_cards = flashcard_dp_info(message.from_user.id)
    mes_print = 'id     :     front     :      back\n'
    for i in all_cards:
        mes_print += f'{i[0]}: {i[1]} - {i[2]}\n'

    await message.answer(mes_print)


class FlashcardManaging(StatesGroup):
    flashcards_managing_create_middle = State()
    flashcards_managing_create_middle_2 = State()
    flashcards_managing_create_end = State()

    flashcards_managing_del_end = State()


def register_handlers_flashcards_managing(dp: Dispatcher):
    dp.register_message_handler(flashcards_managing_start, commands='flc_mg', state='*')
    dp.register_message_handler(flashcards_managing_start,
                                Text(equals=emoji.emojize(":gear:") + " Управление карточками"), state='*')
    dp.register_message_handler(flashcards_managing_create_start,
                                Text(equals=emoji.emojize(":pencil2:") + ' Создать карточку'), state='*')
    dp.register_message_handler(flashcards_managing_del_start,
                                Text(equals=emoji.emojize(":stop_sign:") + ' Удалить карточку'), state='*')
    dp.register_message_handler(flashcards_managing_info,
                                Text(equals=emoji.emojize(":information_source:") + ' Информация о карточках'),
                                state='*')

    dp.register_message_handler(flashcards_managing_create_middle,
                                state=FlashcardManaging.flashcards_managing_create_middle)
    dp.register_message_handler(flashcards_managing_create_middle_2,
                                state=FlashcardManaging.flashcards_managing_create_middle_2)
    dp.register_message_handler(flashcards_managing_create_end,
                                state=FlashcardManaging.flashcards_managing_create_end)

    dp.register_message_handler(flashcards_managing_del_end,
                                state=FlashcardManaging.flashcards_managing_del_end)
