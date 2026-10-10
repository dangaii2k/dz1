from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str | None = None
    db_port: str = "5432"
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

if all([settings.db_host, settings.db_user, settings.db_password, settings.db_name]):
    DB_URL = (
        f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
else:
    DB_URL = "sqlite:///./tasks.db"
