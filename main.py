from fastapi import FastAPI
from infrastructure.database.db_config import Base, engine
from contextlib import asynccontextmanager

# Define el manejador de lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):   
    async with engine.begin() as conn:        
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)