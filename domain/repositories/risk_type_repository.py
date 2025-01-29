from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import RiskType
from domain.entities.Risk_Type import Risk_Type as RiskTypeEntity

class RiskTypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_risk_type(self, risk_type: RiskTypeEntity) -> RiskTypeEntity:
        stmt = insert(RiskType).values(
            category_id=risk_type.category_id,
            description=risk_type.description
        ).returning(RiskType.id, RiskType.category_id, RiskType.description)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return RiskTypeEntity(
                    id=row.id, 
                    category_id=row.category_id, 
                    description=row.description
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Risk Type already exists or invalid category ID") from e

    async def get_risk_type(self, risk_type_id: int) -> Optional[RiskTypeEntity]:
        stmt = select(RiskType).where(RiskType.id == risk_type_id)
        result = await self.session.execute(stmt)
        risk_type = result.scalar_one_or_none()
        if risk_type:
            return RiskTypeEntity(
                id=risk_type.id,
                category_id=risk_type.category_id,
                description=risk_type.description
            )
        return None

    async def get_all_risk_types(self) -> List[RiskTypeEntity]:
        stmt = select(RiskType)
        result = await self.session.execute(stmt)
        risk_types = result.scalars().all()
        return [
            RiskTypeEntity(
                id=risk.id, 
                category_id=risk.category_id, 
                description=risk.description
            ) for risk in risk_types
        ]

    async def update_risk_type(self, risk_type_id: int, risk_type: RiskTypeEntity) -> Optional[RiskTypeEntity]:
        stmt = update(RiskType).where(RiskType.id == risk_type_id).values(
            category_id=risk_type.category_id,
            description=risk_type.description
        ).returning(RiskType.id, RiskType.category_id, RiskType.description)

        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return RiskTypeEntity(
                id=row.id, 
                category_id=row.category_id, 
                description=row.description
            )
        return None

    async def delete_risk_type(self, risk_type_id: int) -> None:
        stmt = delete(RiskType).where(RiskType.id == risk_type_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Risk Type with id {risk_type_id} not found")
