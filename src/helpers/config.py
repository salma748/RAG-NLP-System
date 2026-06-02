from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_EXTENSIONS: str
    FILE_MAX_SIZE_MB: int

    FILE_CHUNK_SIZE: int

    TEXT_CHUNK_SIZE: int
    TEXT_CHUNK_OVERLAP: int
    INDEX_BATCH_SIZE: int = 100
    MONGODB_URI: str
    MONGODB_DB_NAME: str

    OPENAI_API_KEY: str
    OPENAI_API_BASE: str

    GENERATE_RESPONSE_MODEL: str
    EMBEDDINGS_MODEL: str

    EMBEDDING_DIMENSION: int

    MAX_INPUT_TOKENS: int
    MAX_RESPONSE_TOKENS: int

    TEMPERATURE: float

    QDRANT_HOST: str
    QDRANT_PORT: int

    VECTOR_DISTANCE_METRIC: str

    FILE_DIR: str = "assets/files"


    class Config:
        env_file = "src/.env"


def get_settings():

    settings = Settings()

    settings.FILE_ALLOWED_EXTENSIONS = (
        settings.FILE_ALLOWED_EXTENSIONS.split(",")
    )

    return settings