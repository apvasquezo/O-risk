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
            name=personal.name,
            position=personal.position,
            area=personal.area,
            process_id=personal.process_id,
            email=personal.email
        ).returning(
            ORMPersonal.id,
            ORMPersonal.name,
            ORMPersonal.position,
            ORMPersonal.area,
            ORMPersonal.process_id,
            ORMPersonal.email
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return PersonalEntity(
                    id=row.id,
                    name=row.name,
                    position=row.position,
                    area=row.area,
                    process_id=row.process_id,
                    email=row.email
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Error creating personal record") from e

    async def get_personal(self, personal_id: int) -> Optional[PersonalEntity]:
        stmt = select(ORMPersonal).where(ORMPersonal.id == personal_id)
        result = await self.session.execute(stmt)
        orm_personal = result.scalar_one_or_none()
        if orm_personal:
            return PersonalEntity(
                id=orm_personal.id,
                name=orm_personal.name,
                position=orm_personal.position,
                area=orm_personal.area,
                process_id=orm_personal.process_id,
                email=orm_personal.email
            )
        return None

    async def get_all_personal(self) -> List[PersonalEntity]:
        stmt = select(ORMPersonal)
        result = await self.session.execute(stmt)
        orm_personals = result.scalars().all()
        return [
            PersonalEntity(
                id=p.id,
                name=p.name,
                position=p.position,
                area=p.area,
                process_id=p.process_id,
                email=p.email
            ) for p in orm_personals
        ]

    async def update_personal(self, personal_id: int, personal: PersonalEntity) -> Optional[PersonalEntity]:
        stmt = update(ORMPersonal).where(ORMPersonal.id == personal_id).values(
            name=personal.name,
            position=personal.position,
            area=personal.area,
            process_id=personal.process_id,
            email=personal.email
        ).returning(
            ORMPersonal.id,
            ORMPersonal.name,
            ORMPersonal.position,
            ORMPersonal.area,
            ORMPersonal.process_id,
            ORMPersonal.email
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return PersonalEntity(
                id=row.id,
                name=row.name,
                position=row.position,
                area=row.area,
                process_id=row.process_id,
                email=row.email
            )
        return None

    async def delete_personal(self, personal_id: int) -> None:
        stmt = delete(ORMPersonal).where(ORMPersonal.id == personal_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Personal record with id {personal_id} not found")