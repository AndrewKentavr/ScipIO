from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from handlers.keyboards.default.admin_menu import choose_category
from data_b.dp_control import del_task


async def del_task_start(message: types.Message):
    await message.answer('Выберете', reply_markup=choose_category())
    await admin_del_task.name_category.set()


async def del_task_middle(message: types, state: FSMContext):
    await message.answer('Введите название или id задачи', reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(category=message.text)
    await admin_del_task.name_task.set()


async def del_task_end(message: types, state: FSMContext):
    msg = message.text
    user_data = await state.get_data()
    category = user_data['category']
    print(category)
    try:
        del_task(msg, category)
        await message.answer('Задача успешно удалена')
    except:
        await message.answer('Что-то пошло не так')


class admin_del_task(StatesGroup):
    name_category = State()
    name_task = State()


def register_handlers_del_task(dp: Dispatcher):
    dp.register_message_handler(del_task_start, Text(equals="Удалить задачу"), state='*')
    dp.register_message_handler(del_task_middle, state=admin_del_task.name_category)
    dp.register_message_handler(del_task_end, state=admin_del_task.name_task)
