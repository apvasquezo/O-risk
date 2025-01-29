from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Role
from domain.entities.Role import Role as RoleEntity

class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_role(self, role: RoleEntity) -> RoleEntity:
        stmt = insert(Role).values(name=role.name).returning(Role.id, Role.name)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return RoleEntity(id=row.id, name=row.name)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Role with this name already exists") from e

    async def get_role(self, role_id: int) -> Optional[RoleEntity]:
        stmt = select(Role).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()
        return role

    async def get_all_roles(self) -> List[RoleEntity]:
        stmt = select(Role)
        result = await self.session.execute(stmt)
        roles = result.scalars().all()
        return roles

    async def update_role(self, role_id: int, role: RoleEntity) -> Optional[RoleEntity]:
        stmt = update(Role).where(Role.id == role_id).values(name=role.name).returning(Role.id, Role.name)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return RoleEntity(id=row.id, name=row.name)
        return None

    async def delete_role(self, role_id: int) -> None:
        stmt = delete(Role).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Role with id {role_id} not found")