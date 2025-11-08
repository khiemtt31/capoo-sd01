from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/capoo_db"
    
    # JWT settings (Placeholder values, should be loaded from Vault/Env in production)
    SECRET_KEY: str = "SUPER_SECRET_KEY_PLACEHOLDER"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application settings
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Capoo Backend"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()