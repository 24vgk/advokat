from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, LabeledPrice, PreCheckoutQuery,ContentType, InputMediaPhoto, InputMediaVideo
from aiogram.filters import CommandStart, Text, Command, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from magic_filter import F

from keyboards.inline.keyboard import create_inline_kb, create_inline_kb_linc, create_key_kb_inside
from lexicon_src import LEXICON_SRC_MENU_RU, LEXICON_SRC_CONTACT, LEXICON_SRC_ANKETA, LEXICON_SRC_ANKETA_BUTTON

# Инициализируем роутер уровня модуля
router: Router = Router()
# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

keyboards_start = create_key_kb_inside(1, **LEXICON_SRC_MENU_RU)
keyboards_contact = create_inline_kb_linc(2, **LEXICON_SRC_CONTACT)
keyboards_anketa = create_inline_kb(1, **LEXICON_SRC_ANKETA_BUTTON)


class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_FIO = State()        # Состояние ожидания ввода имени
    fill_phon = State()         # Состояние ожидания ввода возраста
    fill_problem = State()      # Состояние ожидания выбора пола


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('"HIRAM" - это юридические решения для организаций и физических лиц. \n\n'
                         'Для ознакомления с информацией о нас перейдите по ссылкам:',
                         reply_markup=keyboards_contact)
    await message.answer('С целью подбора специалиста необходимо заполнить анкету:', reply_markup=keyboards_start)


@router.message(Command(commands='my_id'))
async def menu(message: Message):
    await message.answer(str(message.from_user.id))


@router.callback_query(Text(text='last_btn'))
async def contact(callback: CallbackQuery):
    await callback.message.edit_text('HIRAM - юридические решения для организаций и физических лиц \n'
                                     'Перейдите на сайт и получите консультацию от наших специалистов👇🏽\n\n',
                                     reply_markup=keyboards_contact)


@router.callback_query(Text(text='2'))
async def contact(callback: CallbackQuery):
    await callback.message.edit_text('Cвязаться с нами', reply_markup=keyboards_contact)


# @router.message(Text(text='Заполнить анкету'))
# async def contact(message: Message):
#     await message.answer(LEXICON_SRC_ANKETA['11'], reply_markup=keyboards_anketa)


@router.message(Text(text='Заполнить анкету'))
async def contact1(message: Message, state: FSMContext):
    # await callback.message.edit_text('', reply_markup=keyboards_anketa)
    await message.answer(LEXICON_SRC_ANKETA['11'])
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_FIO)


@router.message(StateFilter(FSMFillForm.fill_FIO))
async def contact(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(fio=message.text)
    await message.answer(text='2. Номер телефона для связи:')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_phon)


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_phon), lambda x: x.text.isdigit() and len(x.text) == 11)
async def contact(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(phon=message.text)
    await message.answer(text='3. Кратко опишите ситуацию:')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_problem)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_phon))
async def warning_not_age(message: Message):
    await message.answer(
        text='Телефон должен быть в формате 89001234567')


@router.message(StateFilter(FSMFillForm.fill_problem))
async def contact(message: Message, state: FSMContext, bot: Bot):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(problem=message.text)
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await message.answer(text='Спасибо, передали данные специалистам, в ближайшее время с Вами свяжутся!')
    if message.from_user.id in user_dict:
        await bot.send_message(5870573729, f'ФИО: {user_dict[message.from_user.id]["fio"]}\n'
                    f'Телефон: {user_dict[message.from_user.id]["phon"]}\n'
                    f'Проблема: {user_dict[message.from_user.id]["problem"]}\n')
