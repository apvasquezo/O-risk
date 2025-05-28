from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.risk_category_repository import RiskCategoryRepository
from application.use_case.manage_riskcategory import ManageRiskCategoriesUseCase
from utils.auth import role_required

router = APIRouter(
    prefix="/risk-categories",
    tags=["Categorías de Riesgo"],
    dependencies=[Depends(role_required("super"))]
)

class RiskCategoryCreate(BaseModel):
    description: str

class RiskCategoryResponse(BaseModel):
    id_riskcategory: int
    description: str

@router.post("/", response_model=RiskCategoryResponse, status_code=201)
async def create_risk_category_endpoint(risk_category: RiskCategoryCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        created = await use_case.create_risk_category(risk_category.description)
        return RiskCategoryResponse(**created.__dict__())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{risk_category_id}", response_model=RiskCategoryResponse)
async def read_risk_category_endpoint(risk_category_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    category = await use_case.get_risk_category(risk_category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return RiskCategoryResponse(**category.model_dump())

@router.get("/", response_model=List[RiskCategoryResponse])
async def read_all_risk_categories_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    categories = await use_case.get_all_risk_categories()
    return [RiskCategoryResponse(**c.__dict__) for c in categories]

@router.put("/{risk_category_id}", response_model=RiskCategoryResponse)
async def update_risk_category_endpoint(risk_category_id: int, risk_category: RiskCategoryCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        updated = await use_case.update_risk_category(risk_category_id, risk_category.description)
        return RiskCategoryResponse(**updated.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{risk_category_id}", response_model=dict)
async def delete_risk_category_endpoint(risk_category_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskCategoryRepository(db)
    use_case = ManageRiskCategoriesUseCase(repository)
    try:
        await use_case.delete_risk_category(risk_category_id)
        return {"detail": "Categoría eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
