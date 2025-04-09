from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

DATABASE_URL = settings.DATABASE_URL  # URL para conexiones asíncronas

print(DATABASE_URL);

# Crea el motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Crea una fábrica de sesiones asíncronas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base para los modelos
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session