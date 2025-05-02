from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "MCP Vehicle Database"
    API_VERSION: str = "1.0.0"
    DATABASE_NAME: str = "C2S"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/{DATABASE_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()