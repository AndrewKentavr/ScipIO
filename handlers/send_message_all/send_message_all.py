import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from config import BOT_TOKEN, ADMINS
from data_b.dp_control import select_all_users
from handlers.keyboards.default.send_message_all import choose_send, add_text

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)


async def send_message_start(message: types.Message, state: FSMContext):
    await message.answer('Введите сообщение для отправки всем', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    if message.text == 'Нет':
        c = []
        await state.update_data(c=c)
    else:
        try:
            c = user_data['c']
            c.append(user_data['msg'])
            await state.update_data(c=c)
        except:
            c = []
            await state.update_data(c=c)
    await send_message_all.main_message1.set()


async def send_dop_msg(message: types, state: FSMContext):
    await state.update_data(msg=message.text)
    await message.answer('Хотите добавить сообщение', reply_markup=add_text())
    await send_message_all.next()


async def send_message_middle(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await state.update_data(msg=message.text)

    c = user_data['c']
    c.append(user_data['msg'])
    await state.update_data(c=c)

    await message.answer('Вы уверенные что хотите отправить это сообщение?', reply_markup=choose_send())
    # await message.answer(f'{c}')
    await send_message_all.next()


async def send_message_end(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Сообщения отправляются', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    c = user_data['c']
    all_users = list(select_all_users())
    for i in range(len(all_users)):
        await asyncio.sleep(0.1)
        user_id = all_users[i][0]
        # if str(user_id) != str(ADMINS):
        for j in range(len(c)):
            await bot.send_message(user_id, c[j])
    await state.finish()


class send_message_all(StatesGroup):
    main_message1 = State()
    main_message2 = State()
    main_message3 = State()


def register_handlers_send_message_all(dp: Dispatcher):
    dp.register_message_handler(send_message_start, Text(equals="Отправка сообщения всем"), state='*')

    dp.register_message_handler(send_message_start, Text(equals="Добавить"), IDFilter(user_id=ADMINS),
                                state=send_message_all.main_message2)

    dp.register_message_handler(send_dop_msg, state=send_message_all.main_message1)

    dp.register_message_handler(send_message_middle,Text(equals="Нет, хочу отправить"), state=send_message_all.main_message2)

    dp.register_message_handler(send_message_end, Text(equals="Да"), state=send_message_all.main_message3)
