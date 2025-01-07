from dataclasses import dataclass

@dataclass
class SettingsTemplate:
    """📝 Templates for settings files"""
    
    PYDANTIC_SETTINGS = """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
"""
