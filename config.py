from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:risk@localhost:5432/riskcontrol"  # ejemplo

    class Config:
        env_file = ".env"

settings = Settings()