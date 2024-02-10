from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str = "postgresql://user:password@127.0.0.1:5432/test"

    class Config:
        env_file = ".env"


settings = Settings()
