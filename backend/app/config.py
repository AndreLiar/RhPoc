from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    # API
    APP_NAME: str = "HR Assistant Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "dev"

    # OpenAI API (Primary AI Provider)
    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"

    # Azure OpenAI (Backup/Optional)
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_CHAT_DEPLOYMENT: str  # e.g. "gpt-4o"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str  # e.g. "text-embedding-3-large"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"

    # Azure Cognitive Search
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_API_KEY: str
    AZURE_SEARCH_INDEX_NAME: str

    # Azure Blob Storage (optional)
    AZURE_BLOB_CONNECTION_STRING: str | None = None
    AZURE_STORAGE_CONTAINER: str | None = None

    # Azure Document Intelligence (optional)
    AZURE_FORMRECOG_ENDPOINT: str | None = None
    AZURE_FORMRECOG_API_KEY: str | None = None

    # Misc
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
