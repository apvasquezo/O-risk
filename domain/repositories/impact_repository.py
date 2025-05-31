from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Impact
from domain.entities.Impact import Impact as ImpactEntity

class ImpactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_impact(self, impact: ImpactEntity) -> ImpactEntity:
        stmt = insert(Impact).values(
            level=impact.level,
            description=impact.description,
            definition=impact.definition,
            criteria_smlv=float(impact.criteria_smlv)
        ).returning(
            Impact.level,
            Impact.description,
            Impact.definition,
            Impact.criteria_smlv
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return ImpactEntity(
                    level=row.level,
                    description=row.description,
                    definition=row.definition,
                    criteria_smlv=row.criteria_smlv
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Impact already exists") from e

    async def get_impact(self, impact_id: int) -> Optional[ImpactEntity]:
        stmt = select(Impact).where(Impact.level == impact_id)
        result = await self.session.execute(stmt)
        impact = result.scalar_one_or_none()
        if impact:
            return ImpactEntity(
                level=impact.level,
                description=impact.description,
                definition=impact.definition,
                criteria_smlv=impact.criteria_smlv
            )
        return None

    async def get_all_impacts(self) -> List[ImpactEntity]:
        stmt = select(Impact)
        result = await self.session.execute(stmt)
        impacts = result.scalars().all()
        return [
            ImpactEntity(
                level=i.level,
                description=i.description,
                definition=i.definition,
                criteria_smlv=i.criteria_smlv
            ) for i in impacts
        ]

    async def update_impact(self, impact_id: int, impact: ImpactEntity) -> Optional[ImpactEntity]:
        stmt = update(Impact).where(Impact.level == impact_id).values(
            level=impact.level,
            description=impact.description,
            definition=impact.definition,
            criteria_smlv=float(impact.criteria_smlv)
        ).returning(
            Impact.level,
            Impact.description,
            Impact.definition,
            Impact.criteria_smlv
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ImpactEntity(
                level=row.level,
                description=row.description,
                definition=row.definition,
                criteria_smlv=row.criteria_smlv
            )
        return None

    async def delete_impact(self, impact_id: int) -> None:
        stmt = delete(Impact).where(Impact.level == impact_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Impact with level {impact_id} not found")