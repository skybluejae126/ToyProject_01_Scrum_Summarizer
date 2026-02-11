import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str
    UPLOAD_DIR: str = "uploads"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# 디버깅을 위한 Loguru 설정
logger.remove()
logger.add(
    sys.stdout, 
    colorize=True, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<magenta>{line}</magenta> - <level>{message}</level>",
    level="DEBUG"
)
logger.add("logs/scrum_debug.log", rotation="10MB", retention="10 days")