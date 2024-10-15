import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import aiohttp
from datetime import datetime

API_TOKEN = '7497152732:AAEJ8jWQjZp6fx49XSQupN1DpICI72rln4I'
WEATHER_API_KEY = '475e0c67d960505af47464bd36f0c7c3'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_last_city = {}


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Узнать погоду"))
    builder.add(KeyboardButton(text="Мой последний город"))
    builder.add(KeyboardButton(text="Помощь"))
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот погоды. Вот что я умею:\n"
        "- Узнать погоду в любом городе\n"
        "- Запомнить ваш последний запрос\n"
        "- Показать прогноз на несколько дней\n\n"
        "Чтобы начать, просто нажмите 'Узнать погоду' или введите название города.",
        reply_markup=get_main_keyboard()
    )


@dp.message(lambda message: message.text == "Узнать погоду")
async def ask_city(message: types.Message):
    await message.reply("Пожалуйста, введите название города:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(lambda message: message.text == "Мой последний город")
async def last_city(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_last_city:
        await get_weather(message, user_last_city[user_id])
    else:
        await message.reply("Вы еще не запрашивали погоду. Пожалуйста, введите название города.")


@dp.message(lambda message: message.text == "Помощь")
async def send_help(message: types.Message):
    await send_welcome(message)


@dp.message()
async def get_weather(message: types.Message, city=None):
    if not city:
        city = message.text

    user_id = message.from_user.id
    user_last_city[user_id] = city

    try:
        weather_url = f'{BASE_URL}appid={WEATHER_API_KEY}&q={city}&units=metric&lang=ru'

        async with aiohttp.ClientSession() as session:
            async with session.get(weather_url) as response:
                weather_data = await response.json()

                if weather_data['cod'] == 200:
                    temperature = weather_data['main']['temp']
                    feels_like = weather_data['main']['feels_like']
                    humidity = weather_data['main']['humidity']
                    description = weather_data['weather'][0]['description']
                    wind_speed = weather_data['wind']['speed']
                    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
                    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')

                    weather_message = (
                        f"🏙 Погода в городе {city}:\n"
                        f"🌡 Температура: {temperature:.1f}°C\n"
                        f"🤔 Ощущается как: {feels_like:.1f}°C\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"🌬 Ветер: {wind_speed} м/с\n"
                        f"☀️ Восход: {sunrise}\n"
                        f"🌅 Закат: {sunset}\n"
                        f"📝 {description.capitalize()}"
                    )

                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Прогноз на 5 дней", callback_data=f"forecast_{city}")]
                    ])

                    await message.answer(weather_message, reply_markup=keyboard)
                else:
                    await message.answer("Извините, не могу найти информацию о погоде для этого города.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await message.answer("Произошла ошибка при получении данных о погоде. Пожалуйста, попробуйте позже.")

    await message.answer("Что еще вы хотите узнать?", reply_markup=get_main_keyboard())


@dp.callback_query(lambda c: c.data and c.data.startswith('forecast_'))
async def process_callback_forecast(callback_query: types.CallbackQuery):
    city = callback_query.data.split('_')[1]
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(forecast_url) as response:
                forecast_data = await response.json()

                if forecast_data['cod'] == '200':
                    forecast_message = f"Прогноз погоды на 5 дней в городе {city}:\n\n"
                    for forecast in forecast_data['list'][::8]:  # Берем прогноз на каждый день (с шагом 24 часа)
                        date = datetime.fromtimestamp(forecast['dt']).strftime('%d.%m')
                        temp = forecast['main']['temp']
                        description = forecast['weather'][0]['description']
                        forecast_message += f"{date}: {temp:.1f}°C, {description}\n"

                    await bot.answer_callback_query(callback_query.id)
                    await bot.send_message(callback_query.from_user.id, forecast_message)
                else:
                    await bot.answer_callback_query(callback_query.id, text="Не удалось получить прогноз погоды.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await bot.answer_callback_query(callback_query.id, text="Произошла ошибка при получении прогноза.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())