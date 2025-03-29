from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:Carpeta24*@localhost:5432/riskmaltern"  
    app_port: str = "8000"  
    db_name: str = "DB" 

    class Config:
        env_file = ".env"

settings = Settings()