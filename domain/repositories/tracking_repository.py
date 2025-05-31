from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Tracking
from domain.entities.Tracking import Tracking as TrackingEntity

class TrackingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tracking(self, tracking: TrackingEntity) -> TrackingEntity:
        stmt = insert(Tracking).values(
            user_id=tracking.user_id,
            control_id=tracking.control_id,
            event_id=tracking.event_id,
            tracking_date=tracking.tracking_date
        ).returning(
            Tracking.id,
            Tracking.user_id,
            Tracking.control_id,
            Tracking.event_id,
            Tracking.tracking_date
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return TrackingEntity(
                    id=row.id,
                    user_id=row.user_id,
                    control_id=row.control_id,
                    event_id=row.event_id,
                    tracking_date=row.tracking_date
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Tracking already exists") from e

    async def get_tracking(self, tracking_id: int) -> Optional[TrackingEntity]:
        stmt = select(Tracking).where(Tracking.id == tracking_id)
        result = await self.session.execute(stmt)
        tracking = result.scalar_one_or_none()
        if tracking:
            return TrackingEntity(
                id=tracking.id,
                user_id=tracking.user_id,
                control_id=tracking.control_id,
                event_id=tracking.event_id,
                tracking_date=tracking.tracking_date
            )
        return None

    async def get_all_trackings(self) -> List[TrackingEntity]:
        stmt = select(Tracking)
        result = await self.session.execute(stmt)
        trackings = result.scalars().all()
        return [
            TrackingEntity(
                id=t.id,
                user_id=t.user_id,
                control_id=t.control_id,
                event_id=t.event_id,
                tracking_date=t.tracking_date
            ) for t in trackings
        ]

    async def update_tracking(self, tracking_id: int, tracking: TrackingEntity) -> Optional[TrackingEntity]:
        stmt = update(Tracking).where(Tracking.id == tracking_id).values(
            user_id=tracking.user_id,
            control_id=tracking.control_id,
            event_id=tracking.event_id,
            tracking_date=tracking.tracking_date
        ).returning(
            Tracking.id,
            Tracking.user_id,
            Tracking.control_id,
            Tracking.event_id,
            Tracking.tracking_date
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return TrackingEntity(
                id=row.id,
                user_id=row.user_id,
                control_id=row.control_id,
                event_id=row.event_id,
                tracking_date=row.tracking_date
            )
        return None

    async def delete_tracking(self, tracking_id: int) -> None:
        stmt = delete(Tracking).where(Tracking.id == tracking_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Tracking with id {tracking_id} not found")