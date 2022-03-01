from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.utils import emoji

from data_b.dp_control import timer_create_dp, timer_info_dp, timer_del_dp
from handlers.keyboards.default import timer_menu


async def timer_select(message: types.Message):
    await message.answer('Выберите:', reply_markup=timer_menu.get_keyboard_timer())


# ----------------------------------CREATE TIMER----------------------------------------
async def timer_create_start(message: types.Message):
    await message.answer('Введите нужное вам время в формате:\n'
                         '<i>16:02</i>\n'
                         'Где <i>16</i> - это часы, а <i>02</i> - минуты\n'
                         '2 пример: <i>05:59</i>', reply_markup=types.ReplyKeyboardRemove())
    await Timer.timer_create_middle.set()


async def timer_create_middle(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    all_timers = timer_info_dp(user_id)

    msg = message.text

    check_func = checking_message(msg)
    if isinstance(check_func, str):  # Проверка на то, что 'check_func' выводит ошибку, типа string
        await message.reply(check_func)
    else:
        # Проверка на то что введеный таймер не существует
        if msg not in all_timers:
            await state.update_data(time=msg)
            await message.answer('Выберите, что вы хотите начать повторять',
                                 reply_markup=timer_menu.get_keyboard_question_tasks())
            await Timer.timer_create_end.set()
        else:
            await message.reply('Такой таймер уже существует')


async def timer_create_end(message: types.Message, state: FSMContext):
    msg = message.text
    if (msg == 'Карточки (Flashcards)') or (msg == 'Математика в уме') or (msg == 'Задачи по математике') or (
            msg == 'Задачи по логике'):
        try:
            user_data = await state.get_data()
            timer_create_dp(message.from_user.id, user_data["time"], msg)
            await message.reply('Таймер успешно установлен', reply_markup=types.ReplyKeyboardRemove())
        except Exception:
            await message.answer(f'Что - то пошло не так')
        await state.finish()

    else:
        await message.reply('Вы написали что-то не то\n'
                            'Нажмите на кнопку, которая вам высветилась ещё раз')
        await Timer.timer_create_end.set()


# ----------------------------------DEL TIMER----------------------------------------

async def timer_del_start(message: types.Message):
    user_id = message.from_user.id
    all_timers = timer_info_dp(user_id)
    if len(all_timers) == 0:
        await message.answer('У вас нет таймеров', reply_markup=types.ReplyKeyboardRemove())
        return

    await message.answer('Удалите таймер, написав номер таймера/таймеров\n'
                         '1 пример: 1\n'
                         '2 пример: 1 3', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Какой из таймеров вы хотите удалить?')

    # Вывод информации о таймерах
    string_timer = ''
    for i in range(len(all_timers)):
        string_timer += f'{i + 1}: {all_timers[i]}\n'

    await message.answer(string_timer)
    await Timer.timer_del.set()


async def timer_del(message: types.Message, state: FSMContext):
    msg = message.text

    id_timer_list_str = checking_message_del(msg)
    # Проверка на то что check_func == True
    if not (isinstance(id_timer_list_str, str)):
        user_id = message.from_user.id
        # Список таймеров пользователя
        all_timers = timer_info_dp(user_id)

        for i in range(len(id_timer_list_str)):
            # Проверка на то что номер введенного таймера существует
            if len(all_timers) >= int(id_timer_list_str[i]) > 0:
                count_id = int(id_timer_list_str[i]) - 1
                timer_del_dp(message.from_user.id, all_timers[count_id])
                await message.answer(f'Таймер {all_timers[count_id]} удалён')
            else:
                await message.answer(f'Таймера под номером {id_timer_list_str[i]} не существует')
                await Timer.timer_del.set()
        await state.finish()
    else:
        await message.reply(id_timer_list_str)
        await Timer.timer_del.set()


# ----------------------------------INFO TIMER----------------------------------------


async def timer_info(message: types.Message):
    user_id = message.from_user.id
    await message.answer('Вот все ваши таймеры:')
    all_timers = timer_info_dp(user_id)
    if len(all_timers) == 0:
        await message.answer('У вас нет таймеров', reply_markup=types.ReplyKeyboardRemove())
        return

    string_timer = ''
    for i in range(len(all_timers)):
        string_timer += f'{i + 1}: {all_timers[i]}\n'

    await message.answer(string_timer)


class Timer(StatesGroup):
    timer_create_middle = State()
    timer_create_end = State()
    timer_del = State()


def checking_message(msg):
    """
    Проверка на то что число написанно вот так:
    13:02
    """
    if ':' in msg:
        c = msg.split(':')
        if len(c) == 2:
            try:
                int(c[0])
                int(c[1])
            except ValueError:
                return 'Введено не число'
            else:
                if len(c[0]) == 2 and len(c[1]) == 2:
                    if (0 <= int(c[0]) < 24) and (0 <= int(c[1]) < 60):
                        return True
                    else:
                        return 'Неправильное время'
                else:
                    return 'Введите числа, как показано в примере'
        else:
            return 'Переборщили со знаками'
    else:
        return 'Забыли про знак ":"'


def checking_message_del(msg):
    """
    Проверка на то что число написанно вот так:
    1 3 или 1
    """
    # Список id таймеров (который ввёл пользователь)
    id_timer_list_str = msg.split()

    for i in range(len(id_timer_list_str)):
        try:
            int(id_timer_list_str[i])
        except ValueError:
            return 'Введено не число'
    return id_timer_list_str


def register_handlers_timer_managing(dp: Dispatcher):
    dp.register_message_handler(timer_create_start,
                                Text(equals=emoji.emojize(":pencil2:") + ' Создать таймер', ignore_case=True))
    dp.register_message_handler(timer_del_start,
                                Text(equals=emoji.emojize(":stop_sign:") + ' Удалить таймер', ignore_case=True))
    dp.register_message_handler(timer_info,
                                Text(equals=emoji.emojize(":information_source:") + ' Посмотреть ваши таймеры',
                                     ignore_case=True))

    dp.register_message_handler(timer_create_middle, state=Timer.timer_create_middle)
    dp.register_message_handler(timer_create_end, state=Timer.timer_create_end)

    dp.register_message_handler(timer_del, state=Timer.timer_del)
