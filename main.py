import asyncio

from app.bot import dp, bot
from app.config import load_config
from app.utils.logger import logger


async def main():
    config = load_config()
    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
