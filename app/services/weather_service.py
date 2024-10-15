import aiohttp

from app.config import load_config
from app.utils.logger import logger


class WeatherService:
    def __init__(self):
        self.config = load_config()
        self.api_key = self.config.OPENWEATHERMAP_API_KEY
        self.base_url = self.config.BASE_URL

    async def get_weather(self, city: str):
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        return await self._make_request(url, params)

    async def get_forecast(self, city: str):
        url = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        data = await self._make_request(url, params)
        return data['list'] if data else None

    async def _make_request(self, url: str, params: dict):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed with status {response.status}: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Error occurred during API request: {e}")
            return None
