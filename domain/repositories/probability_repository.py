from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Probability
from domain.entities.Probability import Probability as ProbabilityEntity

class ProbabilityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_probability(self, probability: ProbabilityEntity) -> ProbabilityEntity:
        stmt = insert(Probability).values(
            level=probability.level,
            description=probability.description,
            definition=probability.definition,
            criteria_smlv=probability.criteria_percentage
        ).returning(
            Probability.id,
            Probability.level,
            Probability.description,
            Probability.definition,
            Probability.criteria_smlv
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return ProbabilityEntity(
                    id=row.id,
                    level=row.level,
                    description=row.description,
                    definition=row.definition,
                    criteria_percentage=float(row.criteria_smlv)
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Probability already exists") from e

    async def get_probability(self, probability_id: int) -> Optional[ProbabilityEntity]:
        stmt = select(Probability).where(Probability.id == probability_id)
        result = await self.session.execute(stmt)
        probability = result.scalar_one_or_none()
        if probability:
            return ProbabilityEntity(
                id=probability.id,
                level=probability.level,
                description=probability.description,
                definition=probability.definition,
                criteria_percentage=float(probability.criteria_smlv)
            )
        return None

    async def get_all_probabilities(self) -> List[ProbabilityEntity]:
        stmt = select(Probability)
        result = await self.session.execute(stmt)
        probabilities = result.scalars().all()
        return [
            ProbabilityEntity(
                id=p.id,
                level=p.level,
                description=p.description,
                definition=p.definition,
                criteria_percentage=float(p.criteria_smlv)
            ) for p in probabilities
        ]

    async def update_probability(self, probability_id: int, probability: ProbabilityEntity) -> Optional[ProbabilityEntity]:
        stmt = update(Probability).where(Probability.id == probability_id).values(
            level=probability.level,
            description=probability.description,
            definition=probability.definition,
            criteria_smlv=probability.criteria_percentage
        ).returning(
            Probability.id,
            Probability.level,
            Probability.description,
            Probability.definition,
            Probability.criteria_smlv
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ProbabilityEntity(
                id=row.id,
                level=row.level,
                description=row.description,
                definition=row.definition,
                criteria_percentage=float(row.criteria_smlv)
            )
        return None

    async def delete_probability(self, probability_id: int) -> None:
        stmt = delete(Probability).where(Probability.id == probability_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Probability with id {probability_id} not found")