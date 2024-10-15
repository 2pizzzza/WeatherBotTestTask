from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENWEATHERMAP_API_KEY: str
    BASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_config() -> Settings:
    return Settings()
