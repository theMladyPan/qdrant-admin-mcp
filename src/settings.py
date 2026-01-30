from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class QdrantSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        extra="ignore",
        case_sensitive=True,
    )

    url: str | None = Field(
        None,
        description="URL of the Qdrant instance",
    )

    api_key: str | None = Field(
        None,
        description="API key for Qdrant instance, if required",
    )


class Settings(BaseSettings):
    logfire_token: str | None = Field(
        None,
        description="Logfire token for logging",
    )

    environment: str = Field(
        "dev",
        description="Environment the application is running in",
    )
    project: str = Field(
        "qdrant-admin-mcp",
        description="Project name",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
