from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:risk@localhost:5432/riskcontrol"  # ejemplo

    print ("estamos en config", DATABASE_URL)
    class Config:
        env_file = ".env"

settings = Settings()