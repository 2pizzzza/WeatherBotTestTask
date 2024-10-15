import asyncio
from app.bot import dp, bot
from app.config import load_config
from app.utils.logger import logger

from app.handlers import start, weather, forecast, help

async def main():
    config = load_config()
    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())