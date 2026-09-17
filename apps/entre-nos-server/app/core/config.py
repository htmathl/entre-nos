from pydantic_settings import BaseSettings, SettingsConfigDict
    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignora variáveis extras que estiverem no .env
    )

    ENV: str = "development"

    # Conexão com Postgres
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "authenticator"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "postgres"

    # Auth GoTrue
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"


settings = Settings()