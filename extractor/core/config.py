from pydantic_settings import BaseSettings

class Config(BaseSettings):

    DOWNLOADS_FOLDER_PATH: str
    LANCE_DB_URI: str
    OPENAI_API_KEY: str

    model_config = {
        "env_file":".env", 
        "extra":"allow"
    }

settings = Config()
