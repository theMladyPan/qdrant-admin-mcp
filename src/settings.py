from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
    )

    url: str = Field(
        ...,
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

    qdrant: QdrantSettings = Field(
        default_factory=QdrantSettings,
        description="Qdrant configuration settings",
    )

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
    )


settings = Settings()
