from aiogram import Bot, Dispatcher
from app.config import load_config

config = load_config()
bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

from app.handlers import start, weather, help
