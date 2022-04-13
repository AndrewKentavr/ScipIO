import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji

from data_b.dp_control import flashcard_dp_create, flashcard_dp_info, flashcard_del, flashcard_setting_photo_text
from handlers.keyboards.default import flashcard_menu
from handlers.keyboards.default.flashcard_menu import get_keyboard_flashcard_start

# Максимальное количество символов на одной стороне
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


# Запист передней стороны
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


# Запист задней стороны
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
    # Если пользователь нажал "да" то при тренировке карточка будет показываться с двух сторон
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
    try:
        flashcard_dp_create(message.from_user.id, user_data["front"], user_data["back"], show_card)
        await message.answer(f'Карточка успешно создана', reply_markup=flashcard_menu.get_keyboard_flashcard_start())
        await message.answer(f'Передняя сторона - {user_data["front"]}\n'
                             f'Задняя сторона - {user_data["back"]}\n'
                             f'Показывать карточку с двух сторон? - {msg}')
    except Exception:
        await message.answer(f'Что - то пошло не так, попробуйте снова')
    await state.finish()


# -----------------------------DEL FUNC-----------------------------------------
async def flashcards_managing_del_start(message: types.Message):
    # Список всех карточек. Пример: [(54, "cat", "кошка"),(55, "dog", "собака")]
    all_cards = flashcard_dp_info(message.from_user.id)
    if len(all_cards) == 0:
        await message.answer(f'У вас нет карточек, которые вы могли бы удалалять\n'
                             f'Сначала создайте их', reply_markup=flashcard_menu.get_keyboard_flashcard_start())
        return

    await message.answer(f'Чтобы удалить карточку - введите её id\n'
                         'Первый пример: 1\n'
                         'Второй пример: 1 2 5',
                         reply_markup=types.ReplyKeyboardRemove())
    # Создание сообщения с информацией о всех каточках
    mes_print = ''
    for i in range(len(all_cards)):
        mes_print += f'{i + 1}:  {all_cards[i][1]}  -  {all_cards[i][2]}\n'

    await message.answer(mes_print)
    await FlashcardManaging.flashcards_managing_del_end.set()


async def flashcards_managing_del_end(message: types.Message, state: FSMContext):
    msg = message.text
    # Список всех карточек. Пример: [(54, "cat", "кошка"),(55, "dog", "собака")]
    all_flash = flashcard_dp_info(message.from_user.id)
    list_id = msg.split()
    list_id = sorted(list_id, reverse=True)
    for card_id in list_id:
        if card_id.isdigit():
            # Провекра что номер меньше чем количество карточек
            if int(card_id) <= len(flashcard_dp_info(message.from_user.id)):
                # Удаление карточки
                # all_flash[int(card_id) - 1][1] - передняя сторона карточки,
                # all_flash[int(card_id) - 1][2] - задняя сторона карточки
                flashcard_del(message.from_user.id, all_flash[int(card_id) - 1][1], all_flash[int(card_id) - 1][2])
                await message.reply(f'Карточка {card_id} успешно удалена', reply_markup=get_keyboard_flashcard_start())

                await state.finish()

            else:
                await message.answer('Такого id карточки - не существует')
                await FlashcardManaging.flashcards_managing_del_end.set()
        else:
            await message.answer('Вы неправильно ввели id карточки\n'
                                 'Напишите как показано в примере:\n'
                                 'Если карточка одна: 1\n'
                                 'Если карточек несколько: 1 2 5\n')
            await FlashcardManaging.flashcards_managing_del_end.set()


async def flashcards_managing_info(message: types.Message):
    if len(flashcard_dp_info(message.from_user.id)) == 0:
        await message.answer('У вас нет карточек')
        return
    else:
        await message.answer('Все ваши карточки:', reply_markup=flashcard_menu.get_keyboard_flashcard_start())
        # Список всех карточек. Пример: [(54, "cat", "кошка"),(55, "dog", "собака")]
        all_cards = flashcard_dp_info(message.from_user.id)
        # Создание сообщения с информацией о всех каточках
        mes_print = ''
        for i in range(len(all_cards)):
            mes_print += f'{i + 1}:  {all_cards[i][1]}  -  {all_cards[i][2]}\n'

        await message.answer(mes_print)


async def setting_show(message: types.Message):
    msg = message.text
    if msg == 'Показ карточек':
        await message.answer('Вы можете настроить показ карточек(flashcards):\n'
                             '1. Сделать показ карточек фотографиями\n'
                             '2. Сделать показ карточек текстом',
                             reply_markup=flashcard_menu.setting_show())
    elif msg == 'Фото':
        flashcard_setting_photo_text(message.from_user.id, 1)
        await message.answer("Показ карточке: Фото", reply_markup=flashcard_menu.get_keyboard_flashcard_start())
    elif msg == 'Текст':
        flashcard_setting_photo_text(message.from_user.id, 0)
        await message.answer("Показ карточке: Текст", reply_markup=flashcard_menu.get_keyboard_flashcard_start())
    return


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
    dp.register_message_handler(setting_show, Text(["Показ карточек", "Фото", "Текст"]), state='*')
