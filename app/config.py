from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://taskflow:taskflow_pass@db:5432/taskflow_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
