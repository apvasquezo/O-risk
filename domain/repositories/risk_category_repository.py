from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import RiskCategory
from domain.entities.Risk_Category import Risk_Category as RiskCategoryEntity

class RiskCategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_risk_category(self, risk_category: RiskCategoryEntity) -> RiskCategoryEntity:
        stmt = insert(RiskCategory).values(
            description=risk_category.description
        ).returning(RiskCategory.id_riskcategory, RiskCategory.description)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return RiskCategoryEntity(id_riskcategory=row.id_riskcategory, description=row.description)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Risk category with this description already exists") from e

    async def get_risk_category(self, category_id: int) -> Optional[RiskCategoryEntity]:
        stmt = select(RiskCategory).where(RiskCategory.id_riskcategory == category_id)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category

    async def get_all_risk_categories(self) -> List[RiskCategoryEntity]:
        stmt = select(RiskCategory)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()
        return categories

    async def update_risk_category(self, category_id: int, risk_category: RiskCategoryEntity) -> Optional[RiskCategoryEntity]:
        stmt = update(RiskCategory).where(RiskCategory.id_riskcategory == category_id).values(
            description=risk_category.description
            ).returning(
                RiskCategory.id_riskcategory, RiskCategory.description
                )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return RiskCategoryEntity(id_riskcategory=row.id_riskcategory, description=row.description)
        return None

    async def delete_risk_category(self, category_id: int) -> None:
        stmt = delete(RiskCategory).where(RiskCategory.id_riskcategory == category_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Risk category with id {category_id} not found")