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
    if message.text == 'Да':
        await message.answer('Чтобы закончить изучение напишите /flash_end')

    elif message.text == 'Правильно' or message.text == 'Неправильно':
        print(message.text)
        if message.text == 'Правильно':
            user_data = await state.get_data()
            if len(user_data) == 0:
                await state.update_data(correct=[])
            correct = user_data['correct']
            correct.append(user_data['card_id'])
    else:
        await message.answer('Вы написали что-то не то')
        await state.finish()
        return

    user_data = await state.get_data()
    card_id, card_front, card_back, show_card = flashcard_generate(message.from_user.id, user_data)
    await message.answer(f'Карточка: {card_id}\n'
                         f'Первая сторона: {card_front}',
                         reply_markup=flashcard_menu.get_keyboard_flashcard_training_game())
    if len(user_data) == 0:
        await state.update_data(correct=[])
    await state.update_data(card_id=card_id)
    await state.update_data(card_back=card_back)

    await Flash_game.fls_game.set()


async def flc_fame_reverse_side(message: types.Message, state: FSMContext):
    print('Обратная сторона')
    user_data = await state.get_data()
    card_back = user_data['card_back']
    await message.answer(f'Обратная сторона: {card_back}')


def flashcard_generate(user_id, user_data):
    user_data = user_data
    if len(user_data) == 0:
        flashcard = flashcard_dp_info_game(user_id, 0)
    else:
        correct = user_data['correct']
        flashcard = flashcard_dp_info_game(user_id, correct)
    return flashcard


class Flash_game(StatesGroup):
    fls_game = State()


def register_handlers_flashcards_training(dp: Dispatcher):
    dp.register_message_handler(flashcards_training_start, commands='flc_train', state='*')
    dp.register_message_handler(flashcards_training_start, Text(equals="Начать учить карточки"), state='*')
    dp.register_message_handler(flc_fame_reverse_side, Text(equals="Обратая сторона"), state='*')
    dp.register_message_handler(fls_game, state=Flash_game.fls_game)
