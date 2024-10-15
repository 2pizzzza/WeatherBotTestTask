from aiogram import types
from aiogram.filters import Command

from app.bot import dp
from app.keyboards.reply import get_main_keyboard


@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Я бот погоды. Вот что я умею:\n"
        "- Узнать погоду в любом городе\n"
        "- Запомнить ваш последний запрос\n"
        "- Показать прогноз на несколько дней\n\n"
        "Чтобы начать, просто нажмите 'Узнать погоду' или введите название города.",
        reply_markup=get_main_keyboard()
    )