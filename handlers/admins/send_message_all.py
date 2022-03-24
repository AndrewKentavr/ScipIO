import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from config import BOT_TOKEN, ADMINS
from data_b.dp_control import dp_admin_stat
from handlers.keyboards.default.admin_menu import choose_send, add_text

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)


async def send_message_start(message: types.Message, state: FSMContext):
    await message.answer('Введите сообщение для отправки всем', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    # Список c - список в котором хранятся все сообщения
    # Если он не существует то он создается и добавляется в state
    try:
        c = user_data['c']
        c.append(user_data['msg'])
        await state.update_data(c=c)
    except:
        c = []
        await state.update_data(c=c)

    await AdminSendMessage.main_message_1.set()


async def send_dop_msg(message: types, state: FSMContext):
    # Добавление сообщения в state
    await state.update_data(msg=message.text)
    await message.answer('Хотите добавить ещё сообщение?', reply_markup=add_text())
    await AdminSendMessage.main_message_2.set()


async def send_message_middle(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await state.update_data(msg=message.text)
    # Добавление последнего сообщеняи в state
    c = user_data['c']
    c.append(user_data['msg'])
    await state.update_data(c=c)

    await message.answer('Вы уверенные что хотите отправить это сообщение?', reply_markup=choose_send())
    await AdminSendMessage.main_message_3.set()


async def send_message_end(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Сообщения отправляются', reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()
    # Все сообщения
    c = user_data['c']
    # Список всех пользователей. Пример: [(id, 'Время регистрации в боте'), (930136261, '2022-03-22 11:29:03.159285')]
    all_users = list(dp_admin_stat())
    for i in range(len(all_users)):
        await asyncio.sleep(0.1)
        user_id = all_users[i][0]
        # if str(user_id) != str(ADMINS):
        for j in range(len(c)):
            try:
                await bot.send_message(user_id, c[j])
            except:
                # Создать удаление пользователей
    await state.finish()


class AdminSendMessage(StatesGroup):
    main_message_1 = State()
    main_message_2 = State()
    main_message_3 = State()


def register_handlers_send_message_all(dp: Dispatcher):
    dp.register_message_handler(send_message_start, Text(equals="Отправка сообщения всем"), state='*')
    dp.register_message_handler(send_dop_msg, state=AdminSendMessage.main_message_1)

    dp.register_message_handler(send_message_start, Text(equals="Добавить"), IDFilter(user_id=ADMINS),
                                state=AdminSendMessage.main_message_2)

    dp.register_message_handler(send_message_middle, Text(equals="Нет, хочу отправить"),
                                state=AdminSendMessage.main_message_2)

    dp.register_message_handler(send_message_end, Text(equals="Да"), state=AdminSendMessage.main_message_3)
