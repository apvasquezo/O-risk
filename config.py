from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:risk@postgres_db:5432/riskcontrol" 
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str    

    print ("estamos en config", DATABASE_URL)
    class Config:
        env_file = ".env"

settings = Settings()

print("Email:", settings.EMAIL_ADDRESS)
print("Clave inicio:", settings.EMAIL_PASSWORD[:4])  # para confirmar que no está vacía