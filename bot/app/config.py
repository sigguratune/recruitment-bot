from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_TELEGRAM_ID: int
    DATABASE_URL: str
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()