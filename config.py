from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:Carpeta24*@localhost:5432/riskcontrol" 

    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str

    print ("estamos en config", DATABASE_URL)
    class Config:
        env_file = ".env"

settings = Settings()