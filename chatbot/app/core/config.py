from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # folder paths
    # DOWNLOADS_FOLDER_PATH: str
    # PROCESSED_FOLDER_PATH: str
    # FAILED_FOLDER_PATH: str

    # LanceDB
    LANCE_DB_URI: str
    LANCE_DB_TABLE_NAME: str

    # Chunking Variables
    # CHUNK_SIZE: int
    # CHUNK_OVERLAP: int

    # OpenAI
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str

    model_config = {
        "env_file":".env", 
        "extra":"allow"
    }

settings = Config()
