from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    PDF_PATH: str
    GROQ_API_KEY: str
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    EMBEDDING_MODEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()