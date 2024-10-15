from aiogram import types
from aiogram.filters import Command

from app.bot import dp
from app.keyboards.inline import get_forecast_keyboard
from app.keyboards.reply import get_main_keyboard
from app.services.weather_service import WeatherService
from app.utils.formatters import format_weather_message
from app.utils.logger import logger

weather_service = WeatherService()
user_last_city = {}


@dp.message(Command(commands=['weather']))
@dp.message(lambda message: message.text == "Узнать погоду")
async def cmd_weather(message: types.Message):
    if message.text == "Узнать погоду":
        await message.reply("Пожалуйста, введите название города:")
        return

    city = message.get_args()
    await process_weather_request(message, city)


@dp.message(lambda message: message.text == "Мой последний город")
async def cmd_last_city(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_last_city:
        await process_weather_request(message, user_last_city[user_id])
    else:
        await message.reply("Вы еще не запрашивали погоду. Пожалуйста, введите название города.")


@dp.message()
async def process_weather_request(message: types.Message, city: str = None):
    if not city:
        city = message.text

    user_id = message.from_user.id
    user_last_city[user_id] = city

    try:
        weather_data = await weather_service.get_weather(city)
        if weather_data:
            weather_message = format_weather_message(city, weather_data)
            await message.reply(weather_message, reply_markup=get_forecast_keyboard(city))
        else:
            await message.reply("Извините, не удалось получить информацию о погоде для этого города.")
    except Exception as e:
        logger.error(f"Error occurred while processing weather request: {e}")
        await message.reply("Произошла ошибка при получении данных о погоде. Пожалуйста, попробуйте позже.")

    await message.answer("Что еще вы хотите узнать?", reply_markup=get_main_keyboard())
