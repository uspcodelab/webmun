from functools import lru_cache
from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app name
    APP_NAME: str = "Meu App FastAPI"
    ENVIRONMENT: str = "development"

    # db config
    DATABASE_URL: SecretStr

    # supabase config
    SUPABASE_URL: AnyHttpUrl
    SUPABASE_ANON_KEY: SecretStr
    SUPABASE_JWT_SECRET: SecretStr
    JWT_ALGORITHM: str = "HS256"

    # pydantic config to read .env files
    model_config = SettingsConfigDict(env_file="../../../.env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()
