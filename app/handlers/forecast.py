from aiogram import types

from app.bot import dp
from app.services.weather_service import WeatherService
from app.utils.formatters import format_forecast_message
from app.utils.logger import logger

weather_service = WeatherService()


@dp.callback_query(lambda c: c.data and c.data.startswith('forecast_'))
async def process_forecast(callback_query: types.CallbackQuery):
    city = callback_query.data.split('_')[1]
    try:
        forecast_data = await weather_service.get_forecast(city)
        if forecast_data:
            forecast_message = format_forecast_message(city, forecast_data)
            await callback_query.answer()
            await callback_query.message.answer(forecast_message)
        else:
            await callback_query.answer("Не удалось получить прогноз погоды.")
    except Exception as e:
        logger.error(f"Error occurred while processing forecast request: {e}")
        await callback_query.answer("Произошла ошибка при получении прогноза. Попробуйте позже.")
