from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
import psycopg2
from psycopg2 import sql
from config import settings
import asyncio
import nest_asyncio
from sqlalchemy import select
from infrastructure.orm.models import Role, User
from infrastructure.orm.base import Base

DATABASE_URL = settings.DATABASE_URL
parsed_url = urlparse(DATABASE_URL)
db_name = parsed_url.path[1:] 
db_user = parsed_url.username
db_password = parsed_url.password
db_host = parsed_url.hostname
db_port = parsed_url.port

def verify_and_create_database():
    """Verifica si la base de datos existe, si no la crea"""
    conn = None
    try:
        # Conectar a la base de datos 'postgres' para verificar/crear la BD objetivo
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()        
        # Verificar si la base de datos existe
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", 
            (db_name,)
        )
        exists = cursor.fetchone()       
        if exists:
            print(f"La base de datos '{db_name}' ya existe.")
        else:
            # Crear la base de datos
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"La base de datos '{db_name}' ha sido creada.")        
        cursor.close()        
    except Exception as e:
        print(f"Error al verificar o crear la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()

# Crear el engine asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear el sessionmaker
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesiones asíncronas"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_models():
    """Inicializa las tablas en la base de datos"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas/verificadas correctamente.")

async def create_default_roles_and_user():
    """Crea los roles y usuario por defecto"""
    async with SessionLocal() as session:
        try:
            print("Verificando existencia de roles...")
            result = await session.execute(
                select(Role).where(Role.id_role.in_([1, 2]))
            )
            roles = result.scalars().all()
            role_ids = [r.id_role for r in roles]
            
            if 1 not in role_ids:
                session.add(Role(id_role=1, name="super", state=True))
                print("Rol 'super' creado.")
            if 2 not in role_ids:
                session.add(Role(id_role=2, name="admin", state=True))
                print("Rol 'admin' creado.")
            await session.commit()           
            print("Verificando existencia del usuario 'Super Visor'...")
            result = await session.execute(
                select(User).where(User.username == "Super Visor")
            )
            existing_user = result.scalar()           
            if not existing_user:
                admin_user = User(
                    username="Super Visor",
                    password="primeravez", 
                    role_id=1  # rol 'super'
                )
                session.add(admin_user)
                await session.commit()
                print("Usuario 'Super Visor' creado correctamente.")
            else:
                print("El usuario 'Super Visor' ya existe.")                
        except Exception as e:
            await session.rollback()
            print(f"Error al crear roles o usuario: {e}")
            raise

async def initialize_database():
    """Función principal para inicializar toda la base de datos"""
    try:
        verify_and_create_database()
        await init_models()
        await create_default_roles_and_user()       
        print("Inicialización de base de datos completada exitosamente.")       
    except Exception as e:
        print(f"Error durante la inicialización: {e}")
        raise

def get_db():
    """Función para obtener sesión de base de datos (para dependency injection)"""
    return get_async_session()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(initialize_database())