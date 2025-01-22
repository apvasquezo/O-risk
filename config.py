from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:123456789@localhost:5432/riskmanegement"  # ejemplo

    class Config:
        env_file = ".env"

settings = Settings()