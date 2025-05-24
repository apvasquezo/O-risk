import asyncio
from sqlalchemy import select
from infrastructure.database.db_config import engine, Base, SessionLocal
from infrastructure.orm.models import User, Role

async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        result = await session.execute(select(Role).where(Role.name.in_(["admin", "super"])))
        existing_roles = result.scalars().all()

        role_names = [r.name for r in existing_roles]
        roles_to_add = []

        if "admin" not in role_names:
            roles_to_add.append(Role(name="admin"))
        if "super" not in role_names:
            roles_to_add.append(Role(name="super"))

        if roles_to_add:
            session.add_all(roles_to_add)
            await session.commit()
            print("Roles insertados.")

        # Buscar el rol 'super' para asociarlo al usuario
        result = await session.execute(select(Role).where(Role.name == "super"))
        super_role = result.scalar_one_or_none()

        # Verifica si el usuario de prueba ya existe
        result = await session.execute(select(User).where(User.username == "Super Visor"))
        existing_user = result.scalar_one_or_none()

        if not existing_user and super_role:
            test_user = User(
                username="Super Visor",
                password="primera vez",
                role_id=super_role.id
            )
            session.add(test_user)
            await session.commit()
            print("Usuario de prueba insertado.")

if __name__ == "__main__":
    asyncio.run(init_db())
