from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://documind:documind123@localhost:5432/documind"
    APP_NAME: str = "DocuMind"
    DEBUG: bool = False
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    COHERE_API_KEY: str = ""
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

