import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory is the project root (one level up from app/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Config:
    """Application configuration loaded from environment variables."""

    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # Absolute path resolutions
    DATA_FILE: Path = BASE_DIR / os.getenv("DATA_FILE_PATH", "data/employees.json")
    LOG_FILE: Path = BASE_DIR / os.getenv("LOG_FILE_PATH", "logs/app.log")


config = Config()