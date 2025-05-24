from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Personal as ORMPersonal
from domain.entities.Personal import Personal as PersonalEntity

class PersonalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_personal(self, personal: PersonalEntity) -> PersonalEntity:
        stmt = insert(ORMPersonal).values(
            id_personal=personal.id_personal,
            name=personal.name,
            position=personal.position,
            area=personal.area,
            email=personal.email
        ).returning(
            ORMPersonal.id_personal,
            ORMPersonal.name,
            ORMPersonal.position,
            ORMPersonal.area,
            ORMPersonal.email
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return PersonalEntity(
                    id_personal=row.id_personal,
                    name=row.name,
                    position=row.position,
                    area=row.area,
                    email=row.email
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Error creating personal record") from e

    async def get_personal(self, personal_id: str) -> Optional[PersonalEntity]:
        stmt = select(ORMPersonal).where(ORMPersonal.id_personal == personal_id)
        result = await self.session.execute(stmt)
        orm_personal = result.scalar_one_or_none()
        if orm_personal:
            return PersonalEntity(
                id_personal=orm_personal.id_personal,
                name=orm_personal.name,
                position=orm_personal.position,
                area=orm_personal.area,
                email=orm_personal.email
            )
        return None

    async def get_all_personal(self) -> List[PersonalEntity]:
        stmt = select(ORMPersonal)
        result = await self.session.execute(stmt)
        orm_personals = result.scalars().all()
        return [
            PersonalEntity(
                id_personal=p.id_personal,
                name=p.name,
                position=p.position,
                area=p.area,
                email=p.email
            ) for p in orm_personals
        ]

    async def update_personal(self, personal_id: str, personal: PersonalEntity) -> Optional[PersonalEntity]:
        stmt = update(ORMPersonal).where(ORMPersonal.id_personal == personal_id).values(
            name=personal.name,
            position=personal.position,
            area=personal.area,
            email=personal.email
        ).returning(
            ORMPersonal.id_personal,
            ORMPersonal.name,
            ORMPersonal.position,
            ORMPersonal.area,
            ORMPersonal.email
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return PersonalEntity(
                id_personal=row.id_personal,
                name=row.name,
                position=row.position,
                area=row.area,
                email=row.email
            )
        return None

    async def delete_personal(self, personal_id: str) -> None:
        stmt = delete(ORMPersonal).where(ORMPersonal.id_personal == personal_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Personal record with id {personal_id} not found")