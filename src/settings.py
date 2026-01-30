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

    url: str = Field(
        "http://localhost:6333",
        description="URL of the Qdrant instance",
    )

    api_key: str | None = Field(
        None,
        description="API key for Qdrant instance, if required, not required for local deployments",
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

    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
