from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import EventLog as ORMEventLog
from domain.entities.Event_Log import EventLog as EventLogEntity

class EventLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_event_log(self, event_log: EventLogEntity) -> EventLogEntity:
        stmt= insert(ORMEventLog).values(
            event_id=event_log.event_id,
            description=event_log.description,
            start_date=event_log.start_date,
            end_date=event_log.end_date,
            discovery_date=event_log.discovery_date,
            accounting_date=event_log.accounting_date,
            amount=event_log.amount,
            recovered_amount=event_log.recovered_amount,
            insurance_recovery=event_log.insurance_recovery,
            risk_factor_id=event_log.risk_factor_id,
            product_id=event_log.product_id,
            process_id=event_log.process_id,
            channel_id=event_log.channel_id,
            city=event_log.city,
            responsible_id=event_log.responsible_id,
            status=event_log.status            
        ).returning(*[c for c in ORMEventLog.__tablen_.columns])
        try:
            result= await self.session.execute(stmt)
            await self.session.commit()
            row= result.fetchone()
            return EventLogEntity(**row._mapping)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError ("Failed to create EventLog") from e
        
    async def get_event_log(self, event_log_id:int) -> Optional[EventLogEntity]:
        stmt = select(ORMEventLog).where(ORMEventLog.id == event_log_id)
        result = await self.session.execute(stmt)
        event_log= result.scalar_one_or_none()
        if event_log:
            return EventLogEntity(**event_log.__dict__)
        return None
    
    async def get_all_event_logs(self) -> List[EventLogEntity]:
        stmt = select(ORMEventLog)
        result = await self.session.execute(stmt)
        event_logs = result.scalars().all()
        return [EventLogEntity(**log.__dict__) for log in event_logs]
    
    async def update_event_log(self, event_log_id:int, event_log: EventLogEntity) -> Optional[EventLogEntity]:
        stmt = update(ORMEventLog).where(ORMEventLog.id == event_log_id).values(
            event_id=event_log.event_id,
            description=event_log.description,
            start_date=event_log.start_date,
            end_date=event_log.end_date,
            discovery_date=event_log.discovery_date,
            accounting_date=event_log.accounting_date,
            amount=event_log.amount,
            recovered_amount=event_log.recovered_amount,
            insurance_recovery=event_log.insurance_recovery,
            risk_factor_id=event_log.risk_factor_id,
            product_id=event_log.product_id,
            process_id=event_log.process_id,
            channel_id=event_log.channel_id,
            city=event_log.city,
            responsible_id=event_log.responsible_id,
            status=event_log.status              
        ).returning(*[c for c in ORMEventLog.__table__.columns])
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return EventLogEntity(**row._mapping)
        return None
    
    async def delete_event_log(self, event_log_id: int) -> None:
        stmt = delete(ORMEventLog).where(ORMEventLog.id == event_log_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"EventLog with id {event_log_id} not found")