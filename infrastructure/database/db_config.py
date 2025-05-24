from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import connect, sql
from psycopg2.errors import DuplicateDatabase
from urllib.parse import urlparse
from config import settings

DATABASE_URL = settings.DATABASE_URL 

parsed_url = urlparse(DATABASE_URL)
db_name = parsed_url.path[1:] 
db_user = parsed_url.username
db_password = parsed_url.password
db_host = parsed_url.hostname
db_port = parsed_url.port

def verify_and_create_database():
    """
    Verifica si la base de datos existe y, si no, la crea.
    """
    try:
        # Conectar al servidor PostgreSQL
        conn = connect(
            dbname="postgres", 
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verificar si la base de datos existe
        cursor.execute(sql.SQL(
            "SELECT 1 FROM pg_database WHERE datname = %s"
        ), [db_name])
        exists = cursor.fetchone()

        if exists:
            print(f"La base de datos '{db_name}' ya existe.")
        else:
            # Crear la base de datos
            cursor.execute(sql.SQL(
                "CREATE DATABASE {}"
            ).format(sql.Identifier(db_name)))
            print(f"La base de datos '{db_name}' ha sido creada.")

    except Exception as e:
        print(f"Error al verificar o crear la base de datos: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

verify_and_create_database()

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
