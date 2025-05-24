import asyncio
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.database.db_config import engine, Base, SessionLocal
from infrastructure.orm.models import User, Role

async def init_db():
    try:
        # Crear todas las tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tablas creadas correctamente.")

        async with SessionLocal() as session:
            try:
                # Verificar roles existentes
                result = await session.execute(select(Role).where(Role.name.in_(["admin", "super"])))
                existing_roles = result.scalars().all()

                role_names = [r.name for r in existing_roles]
                roles_to_add = []

                # Agregar roles si no existen
                if "admin" not in role_names:
                    roles_to_add.append(Role(name="admin", state=True))
                if "super" not in role_names:
                    roles_to_add.append(Role(name="super", state=True))

                if roles_to_add:
                    session.add_all(roles_to_add)
                    await session.commit()
                    print("Roles insertados.")

                # Buscar el rol 'super' para asociarlo al usuario
                result = await session.execute(select(Role).where(Role.name == "super"))
                super_role = result.scalar_one_or_none()

                if not super_role:
                    print("El rol 'super' no se encontró, no se puede insertar el usuario.")
                    return

                # Verificar si el usuario de prueba ya existe
                result = await session.execute(select(User).where(User.username == "Super Visor"))
                existing_user = result.scalar_one_or_none()

                if not existing_user:
                    test_user = User(
                        username="Super Visor",
                        password="primera vez",
                        role_id=super_role.id_role
                    )
                    session.add(test_user)
                    await session.commit()
                    print("Usuario de prueba insertado.")
                else:
                    print("El usuario de prueba ya existe.")
            except SQLAlchemyError as e:
                print(f"Error al gestionar la sesión: {e}")
                await session.rollback()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())
