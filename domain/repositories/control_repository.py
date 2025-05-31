from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Control
from domain.entities.Control import Controller as ControlEntity

class ControlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_control(self, control:ControlEntity) -> ControlEntity:
        stmt= insert(Control).values(
            control_type_id=control.control_type_id,
            description=control.description,
            frequency=control.frequency,
            responsible_id=control.responsible_id
        ).returning(
            Control.id_control, 
            Control.control_type_id, 
            Control.description, 
            Control.frequency, 
            Control.responsible_id
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return ControlEntity(
                    id_control=row.id_control,
                    control_type_id=row.control_type_id,
                    description=row.description,
                    frequency=row.frequency,
                    responsible_id=row.responsible_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError ("Control already exists") from e
        
    async def get_control(self, control_id:int) -> Optional[ControlEntity]:
        stmt = select(Control).where(Control.id == control_id)
        result = await self.session.execute(stmt)
        control= result.scalar_one_or_none()
        if control:
            return ControlEntity(
                id_control=control.id_control,
                control_type_id=control.control_type_id,
                description=control.description,
                frequency=control.frequency,
                responsible_id=control.responsible_id
            )
        return None
    
    async def get_all_controls(self) -> List[ControlEntity]:
        stmt = select(Control)
        result = await self.session.execute(stmt)
        controls = result.scalars().all()
        return [
            ControlEntity(
                id_control= c.id_control,
                control_type_id=c.control_type_id,
                description=c.description,
                frequency=c.frequency,
                responsible_id=c.responsible_id
            ) for c in controls
        ]
        
    async def update_control(self, control_id:int, control:ControlEntity) ->Optional[ControlEntity]:
        stmt = update(Control).where(Control.id_control == control_id).values(
            control_type_id=control.control_type_id,
            description=control.description,
            frequency=control.frequency,
            responsible_id=control.responsible_id
        ).returning(
            Control.id_control,
            Control.control_type_id,
            Control.description,
            Control.frequency,
            Control.responsible_id
        )
        
        result= await self.session.execute(stmt)
        await self.session.commit()
        row= result.fetchone()
        if row:
            return ControlEntity(
                id_control=row.id_control,
                control_type_id=row.control_type_id,
                description=row.description,
                frequency=row.frequency,
                responsible_id=row.responsible_id
            )
        return None
    
    async def delete_control(self, control_id:int) -> None:
        stmt = delete(Control).where(Control.id_control == control_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Control with id {control_id} not found")