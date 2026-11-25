from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings. Values are read from environment variables or the .env file."""

    app_name: str = "Products API"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "shop"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()