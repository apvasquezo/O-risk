from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Cause
from domain.entities.Cause import Cause as CauseEntity

class CauseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_cause(self, cause:CauseEntity)-> CauseEntity:
        stmt=insert(Cause).values(
            description=cause.description,
            risk_factor_id=cause.risk_factor_id,
            event_id=cause.event_id
        ).returing(
            Cause.id,
            Cause.description,
            Cause.risk_factor_id,
            Cause.event_id
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return CauseEntity(
                    id=row.id,
                    description=row.description,
                    risk_factor_id=row.risk_factor_id,
                    event_id=row.event_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Cause already exists") from e
        
    async def get_cause(self, cause_id:int)->Optional[CauseEntity]:
        stmt = select(Cause).where(Cause.id == cause_id)
        result = await self.session.execute(stmt)
        cause= result.scalar_one_or_none()
        if cause:
            return CauseEntity(
                id=cause.id,
                description=cause.description,
                risk_factor_id=cause.risk_factor_id,
                event_id=cause.event_id
            )
        return None
    
    async def get_all_cause(self)->List[CauseEntity]:
        stmt = select(Cause)
        result = await self.session.execute(stmt)
        causes = result.scalars().all()
        return [
            CauseEntity(
                id=c.id,
                description=c.description,
                risk_factor_id=c.risk_factor_id,
                event_id=c.event_id
            ) for c in causes
        ]
        
    async def update_causes(self,cause_id:int, cause:CauseEntity)-> Optional[CauseEntity]:
        stmt = update(Cause).where(Cause.id == cause_id).values(
            description=cause.description,
            risk_factor_id=cause.risk_factor_id,
            event_id=cause.event_id
        ).returning(
            Cause.id,
            Cause.description,
            Cause.risk_factor_id,
            Cause.event_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return CauseEntity(
                id=row.id,
                description=row.description,
                risk_factor_id=row.risk_factor_id,
                event_id=row.event_id
            )
        return None
    
    async def delete_cause(self, cause_id:int)->None:
        stmt = delete(Cause).where(Cause.id == cause_id)
        result= await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Cause with id {cause_id} not found")