from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    LOGFIRE_TOKEN: str | None = None
    ENVIRONMENT: str = "dev"
    PROJECT: str = "qdrant-admin-mcp"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
