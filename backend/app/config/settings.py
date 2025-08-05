import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# ✅ Charger le fichier .env situé dans backend/
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)




class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL: str = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "0").strip() == "1"

    class Config:
        env_file = env_path


# ✅ Instance globale
settings = Settings()
