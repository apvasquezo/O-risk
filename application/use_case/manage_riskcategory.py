from domain.entities.Risk_Category import Risk_Category
from domain.repositories.risk_category_repository import RiskCategoryRepository
from typing import List, Optional

class ManageRiskCategoriesUseCase:
    def __init__(self, repository: RiskCategoryRepository):
        self.repository = repository

    async def create_risk_category(self, description: str) -> Risk_Category:
        # Validar duplicados
        existing_categories = await self.repository.get_all_risk_categories()
        if any(category.description == description for category in existing_categories):
            raise ValueError("A RiskCategory with this description already exists")
        risk_category = Risk_Category(description=description)
        return await self.repository.create_risk_category(risk_category)

    async def get_risk_category(self, risk_category_id: int) -> Optional[Risk_Category]:
        return await self.repository.get_risk_category(risk_category_id)

    async def get_all_risk_categories(self) -> List[Risk_Category]:
        return await self.repository.get_all_risk_categories()

    async def update_risk_category(self, risk_category_id: int, description: str) -> Risk_Category:
        category = await self.repository.get_risk_category(risk_category_id)
        if not category:
            raise ValueError(f"RiskCategory with id {risk_category_id} does not exist")
        updated_category = Risk_Category(id=risk_category_id, description=description)
        return await self.repository.update_risk_category(risk_category_id, updated_category)

    async def delete_risk_category(self, risk_category_id: int) -> None:
        category = await self.repository.get_risk_category(risk_category_id)
        if not category:
            raise ValueError(f"RiskCategory with id {risk_category_id} does not exist")
        await self.repository.delete_risk_category(risk_category_id)
