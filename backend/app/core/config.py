from functools import lru_cache

from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app name
    APP_NAME: str = "WebMUN API"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # list of origins by separated commas (e.g., "app.com,app.xyz")
    CORS_ORIGINS: str = ""

    # db config
    DATABASE_URL: SecretStr

    # supabase config
    SUPABASE_URL: AnyHttpUrl

    REDIS_URL: SecretStr

    @property
    def list_cors_origins(self) -> list[str]:
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

        if self.ENVIRONMENT == "development":
            return ["http://localhost:5173"]

        return origins

    # Host development uses backend/.env; containers and cloud inject process env.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()  # type:ignore
