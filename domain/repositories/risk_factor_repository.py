from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import RiskFactor
from domain.entities.Risk_Factor import Risk_Factory as RiskFactorEntity

class RiskFactorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_risk_factor(self, risk_factor: RiskFactorEntity) -> RiskFactorEntity:
        stmt = insert(RiskFactor).values(
            risk_type_id=risk_factor.risk_type_id,
            description=risk_factor.description
        ).returning(RiskFactor.id_factor, RiskFactor.risk_type_id, RiskFactor.description)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return RiskFactorEntity(
                    id_factor=row.id_factor, 
                    risk_type_id=row.risk_type_id, 
                    description=row.description
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Risk Factor already exists or invalid Risk Type ID") from e

    async def get_risk_factor(self, risk_factor_id: int) -> Optional[RiskFactorEntity]:
        stmt = select(RiskFactor).where(RiskFactor.id_factor == risk_factor_id)
        result = await self.session.execute(stmt)
        risk_factor = result.scalar_one_or_none()
        if risk_factor:
            return RiskFactorEntity(
                id_factor=risk_factor.id_factor,
                risk_type_id=risk_factor.risk_type_id,
                description=risk_factor.description
            )
        return None

    async def get_all_risk_factors(self) -> List[RiskFactorEntity]:
        stmt = select(RiskFactor)
        result = await self.session.execute(stmt)
        risk_factors = result.scalars().all()
        return [
            RiskFactorEntity(
                id_factor=risk.id_factor, 
                risk_type_id=risk.risk_type_id, 
                description=risk.description
            ) for risk in risk_factors
        ]

    async def update_risk_factor(self, risk_factor_id: int, risk_factor: RiskFactorEntity) -> Optional[RiskFactorEntity]:
        stmt = update(RiskFactor).where(RiskFactor.id_factor == risk_factor_id).values(
            risk_type_id=risk_factor.risk_type_id,
            description=risk_factor.description
        ).returning(RiskFactor.id_factor, RiskFactor.risk_type_id, RiskFactor.description)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return RiskFactorEntity(
                id_factor=row.id_factor, 
                risk_type_id=row.risk_type_id, 
                description=row.description
            )
        return None

    async def delete_risk_factor(self, risk_factor_id: int) -> None:
        stmt = delete(RiskFactor).where(RiskFactor.id_factor == risk_factor_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Risk Factor with id {risk_factor_id} not found")