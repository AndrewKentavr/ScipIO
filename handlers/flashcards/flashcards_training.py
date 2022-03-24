"""
Данный алгоритм построен на основе ОДНОГО шага, основной функцией которого является (flc_game)

Основная идея данного алгоритма в том, что из-за того что всё происходит в основной функции, то при нажатии "Правильно"
    и "Неправильно" следующее что делает функция fls_game, это создаёт новую flashcard и вызывает саму себя. Из-за этого
    алгоритм после "Правильно"/"Неправильно" сразу создаёт новую flashcard и показывает её,
     не требуя ввести сообщение от пользователя

Алгоритм работает так:
    Пользователь вызвал /flc_train или нажал на кнопки в боте. Бот спросил готов ли он (flashcards_training_start),
        пользователь ответил, что готов, а дальше вызывается функция flc_game, которая проверяет, что пользователь верно
        нажал на кнопку "Да" и дальше...

    Основной алгоритм. Функция гененирует карточку, присылает пользователю информацию о карточке и создаёт кнопки:
        "Обратная сторона", "Правильно", "Неправильно", а дальше вызывает саму себя, и ждёт следующих действий от
        пользователя:
            1. "Обратная сторона". Тогда вызывается функция flc_game_reverse_side, которая срабатывает
                поверх функции flc_game. Она отправляет пользователю card_back и выключается, STATE оно не меняет!
                flc_game остаётся дальше ждать действий от пользователя

            2. "Правильно" или "Неправильно". При нажатии на кнопку "Правильно" - пользователю при прохождении дальнейшей
                тренировки больше не будет высвечиватся это карточка (карточка удаляется из user_data['flashcards']).
                При нажатии на "Неправильно" - эта карточка при тренировке ещё БУДЕТ показываться

            3. "Закончить". Вызывает функцию flc_game_end, которая присылает статистику пользователю и соответственно
                заканчивает тренировку.
"""
from random import choice

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import emoji

from data_b.dp_control import flashcard_dp_info_game, action_add, flashcard_one
from handlers.keyboards.default import flashcard_menu

from handlers.flashcards.create_flashcard_photo import create_photo
from config import BOT_TOKEN
from aiogram import Bot
import os

from handlers.keyboards.default.flashcard_menu import get_keyboard_flashcard_start, get_keyboard_flashcard_training_game

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)


async def flashcards_training_theory(message: types.Message):
    await message.answer('Флеш-карточки - это удобный способ запоминания и повторения изучаемого материала. '
                         'На одной стороне карточки пишется слово, фраза или термин, а на другой - '
                         'перевод или значение.')
    await message.answer('Чтобы процесс обучения был более эффективным, вы можете придерживаться нескольких советов:')
    await message.answer(
        '1) Разбейте учебные сеансы на отрезки по 10-15 минут, так как их вполне хватит для повторения более 100 слов,'
        ' и такое кол-во свободного времени найдется у любого человека.'
        '\n2) Чаще устраивайте себе экзамены, ведь чем чаще вы будете себя испытывать, тем лучше.'
        '\n3) Создайте подходящую для вас систему обучения, в данном случае дисциплина гораздо полезнее'
        ' случайных занятий.')


async def flashcards_training_start(message: types.Message):
    await message.answer('Принцип работы с карточками и советы /flc_theory')
    await message.answer('Вы готовы?', reply_markup=flashcard_menu.get_keyboard_flashcard_training_start())
    await Flash_game.flc_game.set()


async def flc_game(message: types.Message, state: FSMContext):
    """
    Основной алгоритм

    :param message: Ждёт сообщения: "Да"; "Правильно"; "Неправильно" всё остальное отсекается
    """

    if message.text == 'Да':

        # Генерация массива карточек пользователя
        flashcards = flashcard_generate(message.from_user.id)
        if not flashcards:
            await message.answer('У вас ещё нет карточек', reply_markup=types.ReplyKeyboardRemove())
            await message.answer('Чтобы создать их, вам нужно зайти в '
                                 '"Управление карточками" и нажать на кнопку "Создать карточку"',
                                 reply_markup=get_keyboard_flashcard_start())
            await state.finish()
            return

        await message.answer('Чтобы закончить изучение напишите /flash_end')
        await state.update_data(flashcards=flashcards)
        # Генерация массива правильных карточек (потом для статистики используется)
        await state.update_data(correct=[])

    elif message.text == emoji.emojize(":white_check_mark:") + ' Правильно' or message.text == emoji.emojize(
            ":x:") + ' Неправильно':

        if message.text == emoji.emojize(":white_check_mark:") + ' Правильно':
            user_data = await state.get_data()
            # если "правильно", то в user_data['correct'] добавляется id карточки
            correct = user_data['correct']
            correct.append(user_data['card_id'])
            await state.update_data(correct=correct)

            # удаление карточки из user_data['flashcards']  по его id
            flashcards = user_data['flashcards']
            for i in range(len(flashcards)):
                if user_data['card_id'] == flashcards[i][0]:
                    del flashcards[i]
                    await state.update_data(flashcards=flashcards)
                    break
            # добавление action flc в бд
            action_add(message.from_user.id, 'flc', True)
        else:
            action_add(message.from_user.id, 'flc', False)
    else:
        await message.answer('Вы написали что-то не то')
        return

    user_data = await state.get_data()
    # Выбор РАНДОМНОЙ карточки из user_data['flashcards']
    flashcard = user_data['flashcards']
    #  если карточки закончились то END
    if not flashcard:
        await flc_game_end(message, state)
    else:
        flashcard = choice(flashcard)

        # card_id содежит либо номер карточки, Пример: 54, либо номер каточки и сторону, Пример: 54 обрат.карт
        card_id, card_front, card_back, show_card = flashcard
        list_words = card_front.split()
        card_id_split = str(card_id).split()
        # Если у списка card_id_split существует первый элмент, то значит это обратная сторона
        try:
            str(card_id_split[1])
            side = 'Обратная сторона'
        except:
            side = 'Лицевая сторона'

        await state.update_data(card_id=card_id)
        await state.update_data(card_back=card_back)
        await state.update_data(side=side)
        # Если количество букв будет больше 250, то сообщение будет в виде обычного текста(не в виде фото)
        if (len(list_words) == 1 and len(list_words[0]) <= 50) or (len(list_words) > 1 and len(card_front) <= 250):

            create_photo(card_front, message.from_user.id)
            photo = open(f'handlers/flashcards/{message.from_user.id}.png', 'rb')

            await bot.send_photo(message.chat.id, photo=photo, caption=side, reply_markup=get_keyboard_flashcard_training_game())

            os.remove(f'handlers/flashcards/{message.from_user.id}.png')
        else:
            await message.answer(f'{side}:\n{card_back}',
                                 reply_markup=flashcard_menu.get_keyboard_flashcard_training_game())

        await Flash_game.flc_game.set()


async def flc_game_end(message: types.Message, state: FSMContext):
    """
    Функция присылает статистику по тренировке и закачивает тренировку

    Вызов: 1.Если написали /flash_end
           2.Если закончились flashcards у пользователя
           3. Нажали на кнопку закончить

    :return: Конец тренировки, state.finish()
    """
    await message.answer('Тренировка карточек закончена',
                         reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    correct = user_data['correct']
    # Создание статистики
    string_correct = ''
    for i in range(len(correct)):
        if type(correct[i]) == int:
            # Пример списка info_one_card: [55, "cat", "кошка"] или ["55 обрат.карт", "dog", "собака"]
            info_one_card = flashcard_one(message.from_user.id, correct[i])[0]
            string_correct += f"<u>{i + 1}</u>: {info_one_card[1]} <u><b>=></b></u> {info_one_card[2]}\n"
        else:
            info_one_card = flashcard_one(message.from_user.id, correct[i].split()[0])[0]
            string_correct += f"<u>{i + 1}</u>: {info_one_card[2]} <u><b>=></b></u> {info_one_card[1]}\n"

    await message.answer(emoji.emojize(":bar_chart:") + f' Количество правильно отвеченных карточек: {len(correct)}\n'
                                                        f'{string_correct}')
    await state.finish()


async def flc_game_reverse_side(message: types.Message, state: FSMContext):
    """
    Показ обратной стороны
    """
    user_data = await state.get_data()
    card_back = user_data['card_back']
    list_words = card_back.split()
    side = user_data['side']
    if side == 'Лицевая сторона':
        side = 'Обратная сторона'
    else:
        side = 'Лицевая сторона'

    if (len(list_words) == 1 and len(list_words[0]) <= 50) or (len(list_words) > 1 and len(card_back) <= 250):

        create_photo(card_back, message.from_user.id)
        photo = open(f'handlers/flashcards/{message.from_user.id}.png', 'rb')

        await bot.send_photo(message.chat.id, photo=photo, caption=side)

        os.remove(f'handlers/flashcards/{message.from_user.id}.png')
    else:
        await message.answer(f'{side}:\n{card_back}',
                             reply_markup=flashcard_menu.get_keyboard_flashcard_training_game())
    await Flash_game.flc_game.set()


def flashcard_generate(user_id):
    """

    :return: массив карточек + карточки, которые должны показываться в обратную сторону
    """
    flashcards = flashcard_dp_info_game(user_id)
    if len(flashcards) == 0:
        return False
    flashcards_2 = []
    for i in flashcards:
        if i[3] == True:
            flashcards_2.append((str(i[0]) + ' обрат.карт', i[2], i[1], i[3]))
    return flashcards + flashcards_2


class Flash_game(StatesGroup):
    flc_game = State()


def register_handlers_flashcards_training(dp: Dispatcher):
    dp.register_message_handler(flashcards_training_theory, commands='flc_theory', state='*')
    dp.register_message_handler(flashcards_training_start, commands='flc_train', state='*')
    dp.register_message_handler(flc_game_end, commands='flash_end', state='*')

    # Вот тут проблема с тем, что если писать "Закончить", то конец программы mentally_math
    dp.register_message_handler(flc_game_end, Text(equals="Закончить тренировку"), state='*')

    dp.register_message_handler(flc_game_reverse_side, Text(equals="Обратная сторона"), state='*')
    dp.register_message_handler(flashcards_training_start,
                                Text(equals=emoji.emojize(":brain:") + ' Начать учить карточки'), state='*')
    dp.register_message_handler(flc_game, state=Flash_game.flc_game)
