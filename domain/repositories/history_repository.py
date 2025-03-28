from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import History as ORMHistory
from domain.entities.History import History as HistoryEntity

class HistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_history(self, history: HistoryEntity) -> HistoryEntity:
        stmt = insert(ORMHistory).values(
            eventlog_id=history.eventlog_id,
            control_id=history.control_id,
            star_date=history.start_date,
            end_date=history.end_date,
            value_risk=history.value_risk
        ).returning(
            ORMHistory.id,
            ORMHistory.eventlog_id,
            ORMHistory.control_id,
            ORMHistory.star_date,
            ORMHistory.end_date,
            ORMHistory.value_risk
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return HistoryEntity(
                    id=row.id,
                    eventlog_id=row.eventlog_id,
                    control_id=row.control_id,
                    start_date=row.star_date,
                    end_date=row.end_date,
                    value_risk=row.value_risk
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("History already exists") from e

    async def get_history(self, history_id: int) -> Optional[HistoryEntity]:
        stmt = select(ORMHistory).where(ORMHistory.id == history_id)
        result = await self.session.execute(stmt)
        history = result.scalar_one_or_none()
        if history:
            return HistoryEntity(
                id=history.id,
                eventlog_id=history.eventlog_id,
                control_id=history.control_id,
                start_date=history.star_date,
                end_date=history.end_date,
                value_risk=history.value_risk
            )
        return None

    async def get_all_histories(self) -> List[HistoryEntity]:
        stmt = select(ORMHistory)
        result = await self.session.execute(stmt)
        histories = result.scalars().all()
        return [
            HistoryEntity(
                id=h.id,
                eventlog_id=h.eventlog_id,
                control_id=h.control_id,
                start_date=h.star_date,
                end_date=h.end_date,
                value_risk=h.value_risk
            ) for h in histories
        ]

    async def update_history(self, history_id: int, history: HistoryEntity) -> Optional[HistoryEntity]:
        stmt = update(ORMHistory).where(ORMHistory.id == history_id).values(
            eventlog_id=history.eventlog_id,
            control_id=history.control_id,
            star_date=history.start_date,
            end_date=history.end_date,
            value_risk=history.value_risk
        ).returning(
            ORMHistory.id,
            ORMHistory.eventlog_id,
            ORMHistory.control_id,
            ORMHistory.star_date,
            ORMHistory.end_date,
            ORMHistory.value_risk
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return HistoryEntity(
                id=row.id,
                eventlog_id=row.eventlog_id,
                control_id=row.control_id,
                start_date=row.star_date,
                end_date=row.end_date,
                value_risk=row.value_risk
            )
        return None

    async def delete_history(self, history_id: int) -> None:
        stmt = delete(ORMHistory).where(ORMHistory.id == history_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"History with id {history_id} not found")