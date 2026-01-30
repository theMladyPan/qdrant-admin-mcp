from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
    )


settings = Settings()
