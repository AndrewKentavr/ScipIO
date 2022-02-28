from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.utils import emoji


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    photo = InputFile("data/text_scipio.jpg")
    await message.answer_photo(photo=photo)
    await message.answer(f'Приветствуем на нашем обучающем проекте!' + emoji.emojize(":fire:"))
    await message.answer(
        f'Мы создали его для людей, которые хотят развить свои навыки или получить новые. ' + emoji.emojize(
            ":mortar_board:"))
    await message.answer(f'В функционал проекта входят:'
                         f'\n <b>1)</b> Математические задачи. Категории (Алгебра, Текстовые задачи, Тригонометрия, Вероятность и т.д) ' + emoji.emojize(
        ":book:") +
                         f'\n <b>2)</b> Математические примеры для подсчёта в уме ' + emoji.emojize(":brain:") +
                         f'\n <b>3)</b> Задачи на логику (данетки, загадки, логические задачи) ' + emoji.emojize(
        ":book:") +
                         f'\n <b>4)</b> Пользовательские карточки для обучения ' + emoji.emojize(":label:") +
                         f'\n <b>5)</b> Таймер с оповещениями о занятиях ' + emoji.emojize(":clock1:"))

    await message.answer(f'Основные команды для взаимодействия с ботом:'
                         f'\n <b>1)</b> /math - Задачи по математике'
                         f'\n <b>2)</b> /logic - Задачи на логику'
                         f'\n <b>3)</b> /flashcard - Пользовательские карточки'
                         f'\n <b>4)</b> /timer - Таймер'
                         f'\n <b>5)</b> /help - Просмотр и описание всей информации'
                         f'\n <b>6)</b> /cancel - Отмена текущего действия')

    await message.answer(
        emoji.emojize(
            ":gear:") + f' Это только первая версия (V.1.0), в дальнейшем проект будет улучшаться, и функционал будет расширяться.\n'
                        f'Наша команда: ' + emoji.emojize(":busts_in_silhouette:") + '\n'
                     f'· Андрей Тощаков - создатель всего и вся этого проекта\n'
                     f'· Шагбанов Ахмед - управление и создание данных\n'
                     f'· Игорь Сиверский - помощь в управлении с данными\n'
                     f'· Антон Волынцев - помощь в создании проекта\n'
                     f'· Жанна Клыпо - создание логотипа и т.д\n'                                                              
                     f'· Максим Монахов - помощь в создании текстов и статей для бота\n')


async def cmd_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Основные команды:"
                          f"\n <b>1)</b> /cancel - Отмена текущего действия. <b>Если бот не работает, то после ввода "
                         f"этой функции, программа починиться</b>" + emoji.emojize(":stop_sign:") +

                         f"\n\n <b>2)</b> /math - Задачи по математике. В данном алгоритме вы вибираете категорию задания,"
                         f" а потом просто проходите и нарешиваете соответствующие задания" + emoji.emojize(":book:") +

                         f"\n\n <b>3)</b> /logic - Задачи на логику. Тоже самое что и задачи по математике, только другие"
                         f" категории заданий" + emoji.emojize(":book:") +

                         f"\n\n <b>4)</b> /flashcard - Пользовательские карточки. Флеш-карточки - это удобный способ "
                         f"запоминания и повторения изучаемого материала. На одной стороне карточки пишется слово, "
                         f"фраза или термин, а на другой - перевод или значение." + emoji.emojize(":label:") +

                         f"\n\n <b>5)</b> /timer - Таймер. Вы можете поставить время выполнения определйнных заданий. "
                         f"Например: вы хотите, чтобы в 08:30 утра, вы стабильно тренировали карточки, тогда вам необходимо сделать следующие действия:\n"
                         f"Прописать /timer --> нажать на 'Создать таймер' --> Ввести нужное время --> Всё, готово, таймер создан! " + emoji.emojize(":clock1:"),
                         reply_markup=types.ReplyKeyboardRemove())

    await message.answer('Второстепенные команды:'
                         '\n <b>1)</b> /start - Покажет начально сообщение бота'
                         '\n <b>2)</b> /equation_mentally - тренировка для подсчёта в уме'
                         '\n <b>3)</b> /mell_theory - теория для подсчёта в уме'
                         '\n <b>4)</b> /flc_mg - управление карточек'
                         '\n <b>5)</b> /flc_train - тенировка с карточками'
                         '\n <b>6)</b> /flc_theory - теория по карточкам')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_start(dp: Dispatcher):
    global dp_main
    dp_main = dp
    dp.register_message_handler(cmd_start, CommandStart(), state='*')
    dp.register_message_handler(cmd_help, CommandHelp(), state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
