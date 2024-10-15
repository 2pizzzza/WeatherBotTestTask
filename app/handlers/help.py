from aiogram import types
from aiogram.filters import Command

from app.bot import dp
from app.keyboards.reply import get_main_keyboard


@dp.message(Command(commands=['help']))
@dp.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    await message.reply(
        "Вот что я умею:\n"
        "- /weather [город] - узнать погоду в указанном городе\n"
        "- 'Мой последний город' - узнать погоду в последнем запрошенном городе\n"
        "- 'Прогноз на 5 дней' - получить прогноз погоды на 5 дней вперед\n\n"
        "Если у вас есть вопросы, не стесняйтесь спрашивать!",
        reply_markup=get_main_keyboard()
    )
