from datetime import datetime


def format_weather_message(city: str, weather_data: dict) -> str:
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')

    return (
        f"🏙 Погода в городе {city}:\n"
        f"🌡 Температура: {temperature:.1f}°C\n"
        f"🤔 Ощущается как: {feels_like:.1f}°C\n"
        f"💧 Влажность: {humidity}%\n"
        f"🌬 Ветер: {wind_speed} м/с\n"
        f"☀️ Восход: {sunrise}\n"
        f"🌅 Закат: {sunset}\n"
        f"📝 {description.capitalize()}"
    )


def format_forecast_message(city: str, forecast_data: list) -> str:
    message = f"Прогноз погоды на 5 дней в городе {city}:\n\n"
    for forecast in forecast_data:
        date = datetime.fromtimestamp(forecast['dt']).strftime('%d.%m')
        temp = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        message += f"{date}: {temp:.1f}°C, {description}\n"
    return message
