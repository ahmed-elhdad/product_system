from pydantic_settings import BaseSettings
from typing import List, Optional
import os




class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    MONGODB_USERNAME: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None
    MONGODB_URI: Optional[str] = None

    FILE_MAX_SIZE: int
    FILE_ALLOWED_IMAGES_TYPES: List[str]

    UPLOAD_DIR: str 

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


def get_settings():
    return Settings()
