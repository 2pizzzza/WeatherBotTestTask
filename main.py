import asyncio
from app.bot import dp, bot
from app.config import load_config
from app.utils.logger import logger
from app.handlers import start, weather, forecast, help
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading


#Большинство кода здесь для того чтобы он работал
# на сервере, потому что на сервер который я задеплоил нужен
# что то вроде backroud work с портом
def run_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Starting HTTP server on port 8080...")
    httpd.serve_forever()

async def main():
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

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
