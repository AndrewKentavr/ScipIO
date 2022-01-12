"""
Данный алгоритм построен на основе ОДНОГО шага, основной функцией которого является (fls_game)

Оснавная идея данного алгоритма в том, что из-за того что всё происходит в основной функции, то при нажатии "Правильно"
    и "Неправильно" следующее что делает функция fls_game, это создаёт новую flashcard и вызывает саму себя. Из-за этого
    алгоритм после "Правильно"/"Неправильно" сразу создаёт новую flashcard

Алгоритм работает так:
    Пользователь вызвал /flc_train или нажал на кнопки в боте. Бот спросил готов ли он (flashcards_training_start),
        пользователь ответил, что готов, а дальше вызывается функция fls_game, которая проверяет, что пользователь верно
        нажал на кнопку "Да" и дальше...

    Основной алгоритм. Функия гененирует карточку, присылает пользователю информацию о карточке и создаёт кнопки:
        "Обратная сторона", "Правильно", "Неправильно", а дальше вызывает саму себя, и ждёт следующих дейстрий от
        пользователя:
            1. "Обратная сторона". Тогда вызывается функция flc_game_reverse_side, которая срабатывает
                поверх функции fls_game. Она отправляет пользователю card_back и выключается, STATE оно не меняет!
                fls_game остаётся далье ждать действий от пользователя

            2. "Правильно" или "Неправильно". При нажатии на кнопку "Правильно" - пользователю при прохождении дальнейшей
                тренировки больше не будет высвечиватся это карточка (id карточки добавляется в user_data, где потом
                идёт простая проверка этого массива).
                При нажатии на "Неправильно" - эта карточка при тренировке ещё БУДЕТ показываться

            3. "Закончить". Вызывает функцию flc_game_end, которая присылвает статистику пользователю и соответственно
                заканчивает тренировку.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_b.dp_control import flashcard_dp_info_game
from handlers.keyboards.default import flashcard_menu


async def flashcards_training_start(message: types.Message):
    await message.answer('Лайфхаки для работы с карточками /cards_info')
    await message.answer('Вы готовы?', reply_markup=flashcard_menu.get_keyboard_flashcard_training_start())
    await Flash_game.fls_game.set()


async def fls_game(message: types.Message, state: FSMContext):
    """
    Основной алгоритм

    :param message: Ждёт сообщения: "Да"; "Правильно"; "Неправильно" всё остальное отсекается
    """

    if message.text == 'Да':
        await message.answer('Чтобы закончить изучение напишите /flash_end')

    elif message.text == 'Правильно' or message.text == 'Неправильно':

        # если "правильно", то в user_data['correct'] добавляется id карточки
        if message.text == 'Правильно':
            user_data = await state.get_data()
            correct = user_data['correct']
            correct.append(user_data['card_id'])
            await state.update_data(correct=correct)

    else:
        await message.answer('Вы написали что-то не то')
        await state.finish()
        return

    user_data = await state.get_data()
    # Генерация карточки
    flashcard = flashcard_generate(message.from_user.id, user_data)

    #  если карточки закончились то END
    if not flashcard:
        await flc_game_end(message, state)
    else:
        card_id, card_front, card_back, show_card = flashcard

        # если user_data - пустая, то создаётся массив correct
        if len(user_data) == 0:
            await state.update_data(correct=[])

        await state.update_data(card_id=card_id)
        await state.update_data(card_back=card_back)

        await message.answer(f'Карточка: {card_id}\n'
                             f'Первая сторона: {card_front}',
                             reply_markup=flashcard_menu.get_keyboard_flashcard_training_game())
        await Flash_game.fls_game.set()


async def flc_game_end(message: types.Message, state: FSMContext):
    """
    Функция присылает статистику по тренировке и закачивает тренировку

    Вызов: 1.Если написали /flash_end
           2.Если закончились flashcards у пользователя
           3. Нажали на кнопку закончить

    :return: Конец тренировки, state.finish()
    """
    await message.answer('Тренировка карточек закончена', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    correct = user_data['correct']

    await message.answer(f'Количество правильно отвеченных карточек: {len(correct)}\n'
                         f'Id самих карточек: {[f"{i}, " for i in correct]}')
    await state.finish()


async def flc_game_reverse_side(message: types.Message, state: FSMContext):
    """
    Показ обратной стороны
    """
    user_data = await state.get_data()
    card_back = user_data['card_back']
    await message.answer(f'Обратная сторона: {card_back}')


def flashcard_generate(user_id, user_data):
    user_data = user_data
    if len(user_data) == 0:
        flashcard = flashcard_dp_info_game(user_id, 0)
    else:
        correct = user_data['correct']
        try:
            flashcard = flashcard_dp_info_game(user_id, correct)
        except IndexError:
            return False
    return flashcard


class Flash_game(StatesGroup):
    fls_game = State()


def register_handlers_flashcards_training(dp: Dispatcher):
    dp.register_message_handler(flashcards_training_start, commands='flc_train', state='*')
    dp.register_message_handler(flc_game_end, commands='flash_end', state='*')

    # Вот тут проблема с тем, что если писать "Закончить", то конец программы mentally_math
    dp.register_message_handler(flc_game_end, Text(equals="Закончить тренировку"), state='*')

    dp.register_message_handler(flashcards_training_start, Text(equals="Начать учить карточки"), state='*')
    dp.register_message_handler(flc_game_reverse_side, Text(equals="Обратая сторона"), state='*')
    dp.register_message_handler(fls_game, state=Flash_game.fls_game)
