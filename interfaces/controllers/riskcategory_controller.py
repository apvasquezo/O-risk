from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.risk_category_repository import RiskCategoryRepository
from application.use_case.manage_riskcategory import ManageRiskCategoriesUseCase

router = APIRouter()

class RiskCategoryCreate(BaseModel):
    description: str

class RiskCategoryResponse(BaseModel):
    id_riskcategory: int
    description: str

@router.post("/risk-categories/", response_model=RiskCategoryResponse)
async def create_risk_category(risk_category: RiskCategoryCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        created_risk_category = await use_case.create_risk_category(risk_category.description)
        return RiskCategoryResponse(id_riskcategory=created_risk_category.id, description=created_risk_category.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/risk-categories/{risk_category_id}", response_model=RiskCategoryResponse)
async def read_risk_category(risk_category_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    category = await use_case.get_risk_category(risk_category_id)
    if not category:
        raise HTTPException(status_code=404, detail="RiskCategory not found")
    return RiskCategoryResponse(id_riskcategory=category.id_riskcategory, description=category.description)

@router.get("/risk-categories/", response_model=List[RiskCategoryResponse])
async def read_all_risk_categories(db: AsyncSession = Depends(get_db)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    categories = await use_case.get_all_risk_categories()
    return [RiskCategoryResponse(id_riskcategory=category.id_riskcategory, description=category.description) for category in categories]

@router.put("/risk-categories/{risk_category_id}", response_model=RiskCategoryResponse)
async def update_risk_category(risk_category_id: int, risk_category: RiskCategoryCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        updated_category = await use_case.update_risk_category(risk_category_id, risk_category.description)
        return RiskCategoryResponse(id_riskcategory=updated_category.id_riskcategory, description=updated_category.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/risk-categories/{risk_category_id}", response_model=dict)
async def delete_risk_category(risk_category_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        await use_case.delete_risk_category(risk_category_id)
        return {"detail": "RiskCategory deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))