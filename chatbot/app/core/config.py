from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # LanceDB
    LANCE_DB_URI: str
    LANCE_DB_TABLE_NAME: str

    # OpenAI Model
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENAI_EMBEDDER: str

    DEFAULT_SYSTEM_RULE: str

    model_config = {
        "env_file":".env", 
        "extra":"allow"
    }

settings = Config()
