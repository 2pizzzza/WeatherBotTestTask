from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Узнать погоду"))
    builder.add(KeyboardButton(text="Мой последний город"))
    return builder.as_markup(resize_keyboard=True)
