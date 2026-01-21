from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Databse
    DATABASE_URL: str 
    DB_NAME: str
    DB_USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )

settings = Settings()   # type: ignore
