from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import List, Optional
from infrastructure.orm.models import User as ORMUser
from domain.entities.User import User as UserEntity

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserEntity) -> UserEntity:
        stmt = insert(ORMUser).values(
            username=user.username, 
            password=user.password, 
            role_id=user.role_id
        ).returning(ORMUser.id_user, ORMUser.username, ORMUser.role_id)
        try:
            result = await self.session.execute(stmt)
            print(result)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return UserEntity(
                    id_user=row.id_user, 
                    username=row.username, 
                    password=user.password, 
                    role_id=row.role_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("User with this username already exists") from e

    async def get_user(self, user_id: int) -> Optional[UserEntity]:
        stmt = select(ORMUser).where(ORMUser.id_user == user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        if orm_user:
            return UserEntity(
                id_user=orm_user.id_user, 
                username=orm_user.username, 
                password=orm_user.password, 
                role_id=orm_user.role_id
            )
        return None

    async def get_user_username(self, username: str) -> Optional[UserEntity]:
        print(str(username))
        stmt = select(ORMUser).where(ORMUser.username == username)
        print(str(stmt))
        result = await self.session.execute(stmt)
        print(str(result))
        orm_user = result.scalar_one_or_none()
        
        if orm_user:
            return UserEntity(
                id_user=orm_user.id_user,
                username=orm_user.username,
                password=orm_user.password,
                role_id=orm_user.role_id
            )
        return None

    async def get_all_users(self) -> List[UserEntity]:
        stmt = select(ORMUser)
        result = await self.session.execute(stmt)
        orm_users = result.scalars().all()
        return [
            UserEntity(
                id_user=u.id_user, 
                username=u.username, 
                password=u.password, 
                role_id=u.role_id
            ) for u in orm_users
        ]

    async def update_user(self, user_id: int, user: UserEntity) -> Optional[UserEntity]:
        stmt = update(ORMUser).where(ORMUser.id_user == user_id).values(
            username=user.username, 
            password=user.password, 
            role_id=user.role_id
        ).returning(ORMUser.id_user, ORMUser.username, ORMUser.role_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return UserEntity(
                id_user=row.id_user, 
                username=row.username, 
                password=user.password, 
                role_id=row.role_id
            )
        return None

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(ORMUser).where(ORMUser.id_user == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"User with id {user_id} not found")
