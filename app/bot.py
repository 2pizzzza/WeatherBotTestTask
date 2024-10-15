from aiogram import Bot, Dispatcher
from app.config import load_config

config = load_config()
bot = Bot(token=config.TELEGRAM_BOT_TOKEN, proxy='http://proxy.server:3128')
dp = Dispatcher()
