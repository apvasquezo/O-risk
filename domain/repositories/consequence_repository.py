from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Consequence
from domain.entities.Consequence import Consequence as ConsequenceEntity

class ConsequenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_consequence(self, consequence:ConsequenceEntity)-> ConsequenceEntity:
        stmt=insert(Consequence).values(
            description=consequence.description,
            risk_factor_id=consequence.risk_factor_id,
            event_id=consequence.event_id
        ).returing(
            Consequence.id_consequence,
            Consequence.description,
            Consequence.risk_factor_id,
            Consequence.event_id
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return ConsequenceEntity(
                    id_consequence=row.id_consequence,
                    description=row.description,
                    risk_factor_id=row.risk_factor_id,
                    event_id=row.event_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Consequence already exists") from e
        
    async def get_consequence(self, consequence_id:int)->Optional[ConsequenceEntity]:
        stmt = select(Consequence).where(Consequence.id_consequence == consequence_id)
        result = await self.session.execute(stmt)
        cause= result.scalar_one_or_none()
        if cause:
            return ConsequenceEntity(
                id_consequence=Consequence.id_consequence,
                description=Consequence.description,
                risk_factor_id=Consequence.risk_factor_id,
                event_id=Consequence.event_id
            )
        return None
    
    async def get_all_consequence(self)->List[ConsequenceEntity]:
        stmt = select(Consequence)
        result = await self.session.execute(stmt)
        causes = result.scalars().all()
        return [
            ConsequenceEntity(
                id_consequence=c.id_consequence,
                description=c.description,
                risk_factor_id=c.risk_factor_id,
                event_id=c.event_id
            ) for c in Consequence
        ]
        
    async def update_consequence(self,consequence_id:int, consequence:ConsequenceEntity)-> Optional[ConsequenceEntity]:
        stmt = update(Consequence).where(Consequence.idconsequence == consequence_id).values(
            description=consequence.description,
            risk_factor_id=consequence.risk_factor_id,
            event_id=consequence.event_id
        ).returning(
            Consequence.id_consequence,
            Consequence.description,
            Consequence.risk_factor_id,
            Consequence.event_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ConsequenceEntity(
                id=row.id_consequence,
                description=row.description,
                risk_factor_id=row.risk_factor_id,
                event_id=row.event_id
            )
        return None
    
    async def delete_consequence(self, consequence_id:int)->None:
        stmt = delete(Consequence).where(Consequence.id_consequence == consequence_id)
        result= await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Consequence with id {consequence_id} not found")