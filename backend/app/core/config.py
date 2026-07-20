from functools import lru_cache
from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # app name 
    APP_NAME: str = "Meu App FastAPI"
    ENVIRONMENT: str = "development"
    
    # supabase config
    # SUPABASE_URL: AnyHttpUrl
    # SUPABASE_ANON_KEY: SecretStr
    # SUPABASE_JWT_SECRET: SecretStr
    # JWT_ALGORITHM
    
    # pydantic config to read .env files
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore" 
    )
