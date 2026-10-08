from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    PDF_PATH: str
    GROQ_API_KEY: str
    GROQ_BASE_URL: str
    TOP_K: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    EMBEDDING_MODEL: str
    RERANKING_MODEL: str

    COLLECTION_NAME: str
    CHROMA_DB_PATH: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()