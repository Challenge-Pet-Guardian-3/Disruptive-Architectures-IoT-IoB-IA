from pathlib import Path
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_TITLE: str = "Guardian AI API"
    APP_DESCRIPTION: str = "Microserviço de Inteligência Artificial Generativa e RAG para o ecossistema PetGuardian (Challenge Clyvo 2026)"
    APP_VERSION: str = "1.0.0"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    
    # ChromaDB RAG
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "data" / "chroma_db")
    KNOWLEDGE_BASE_DIR: str = str(BASE_DIR / "app" / "data" / "knowledge_base")
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
