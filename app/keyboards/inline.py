from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_forecast_keyboard(city: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прогноз на 5 дней", callback_data=f"forecast_{city}")]
    ])
