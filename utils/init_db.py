import asyncio
from infrastructure.database.db_config import engine, Base 

async def init_db():
    async with engine.begin() as conn:
        # Crea todas las tablas
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())