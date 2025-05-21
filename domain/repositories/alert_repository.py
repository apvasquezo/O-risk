from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Alert
from domain.entities.Alert import Alert as AlertEntity

class AlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_alert(self, alert:AlertEntity)-> AlertEntity:
        stmt=insert(Alert).values(
            title = alert.title,
            message = alert.message,
            is_read = alert.is_read,
            date_created = alert.date_created,
            role_id = alert.role_id,
            type =alert.type,
            eventlog_id = alert.eventlod_id,
            control_id = alert.control_id
        ).returing(
            Alert.title,
            Alert.message,
            Alert.is_read,
            Alert.date_created,
            Alert.role_id,
            Alert.type,
            Alert.eventlog_id,
            Alert.control_id 
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return AlertEntity(
                    title = row.title,
                    message = row.message,
                    is_read = row.is_read,
                    date_created = row.date_created,
                    role_id = row.role_id,
                    type =row.type,
                    eventlog_id = row.eventlod_id,
                    control_id = row.control_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Alert already exists") from e
        
    async def get_alert (self, alert_id: int)-> Optional[AlertEntity]:
        stmt=select(Alert).where(Alert.id_alert==alert_id)
        result=await self.session.execute(stmt)
        alert=result.scalar_one_or_none()
        if alert:
            return AlertEntity(
                title = alert.title,
                message = alert.message,
                is_read = alert.is_read,
                date_created = alert.date_created,
                role_id = alert.role_id,
                type =alert.type,
                eventlog_id = alert.eventlod_id,
                control_id = alert.control_id                
            )
        return None
    
    async def get_all_alert(self)-> List[AlertEntity]:
        stmt=select(Alert)
        result=await self.session.execute(stmt)
        alerts=result.scalars().all()
        return[
            AlertEntity(
                title = a.title,
                message = a.message,
                is_read = a.is_read,
                date_created = a.date_created,
                role_id = a.role_id,
                type =a.type,
                eventlog_id = a.eventlod_id,
                control_id = a.control_id                   
            )for a in alerts
        ]
#las alertas no se actualizan ni se eliminan 