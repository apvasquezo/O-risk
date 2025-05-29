from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Cause
from domain.entities.Cause import Causes as CauseEntity

class CauseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_cause(self, cause:CauseEntity)-> CauseEntity:
        stmt=insert(Cause).values(
            description=cause.description,
            
        ).returning(
            Cause.id_cause,
            Cause.description,
          
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return CauseEntity(
                    id_cause=row.id_cause,
                    description=row.description,
                  
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Cause already exists") from e
        
    async def get_cause(self, cause_id:int)->Optional[CauseEntity]:
        stmt = select(Cause).where(Cause.id_cause == cause_id)
        result = await self.session.execute(stmt)
        cause= result.scalar_one_or_none()
        if cause:
            return CauseEntity(
                id=cause.id,
                description=cause.description,
                
            )
        return None
    
    async def get_all_cause(self)->List[CauseEntity]:
        stmt = select(Cause)
        result = await self.session.execute(stmt)
        causes = result.scalars().all()
        return [
            CauseEntity(
                id_cause=c.id_cause,
                description=c.description,
                
            ) for c in causes
        ]
        
    async def update_causes(self,cause_id:int, cause:CauseEntity)-> Optional[CauseEntity]:
        stmt = update(Cause).where(Cause.id_cause == cause_id).values(
            description=cause.description,
            
        ).returning(
            Cause.id_cause,
            Cause.description,
          
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return CauseEntity(
                id_cause=row.id_cause,
                description=row.description,
               
            )
        return None
    
    async def delete_cause(self, cause_id:int)->None:
        stmt = delete(Cause).where(Cause.id_cause == cause_id)
        result= await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Cause with id {cause_id} not found")