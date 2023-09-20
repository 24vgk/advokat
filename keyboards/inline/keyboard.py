from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, KeyboardButton, InlineQueryResultLocation
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_MENU_COMMANDS_RU

dp: Dispatcher = Dispatcher()


# Функция генерит инлайн-клавиатуру автоматом в зависимости от ЛЕКСИКОНА
def create_inline_kb(width: int, last_btn: str | None = None, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализация билдера
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализация списка кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполнение списка кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_MENU_COMMANDS_RU[button] if button in LEXICON_MENU_COMMANDS_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    # Распаковка списка с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возврат объекта инлайн-клавиатуры
    return kb_builder.as_markup()


def create_key_kb_inside(width: int, *args: str, **kwargs: str):
    # Инициализируем билдер для клавиатуры ADMIN"
    admin_menu_b: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    # # Инициализация списка кнопок
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))
    if kwargs:
        for key, button in kwargs.items():
            buttons.append(KeyboardButton(text=button))

    admin_menu_b.row(*buttons, width=width)
    return admin_menu_b.as_markup(resize_keyboard=True)


def create_link(link, last_btn: str | None = None):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if last_btn:
        kb_builder.row(InlineKeyboardButton(text=last_btn, url=link))
    return kb_builder.as_markup()


def create_inline_kb_linc(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_MENU_COMMANDS_RU[button] if button in LEXICON_MENU_COMMANDS_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=button,
                url=text))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
                            text=last_btn,
                            callback_data='last_btn'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()