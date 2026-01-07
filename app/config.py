import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///genome_guides.db"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"))

_settings = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        print(f"DEBUG: get_settings() loaded SQLALCHEMY_DATABASE_URL: {_settings.SQLALCHEMY_DATABASE_URL}") # Debug print
    return _settings

def reload_settings() -> Settings:
    global _settings
    _settings = Settings()
    return _settings
