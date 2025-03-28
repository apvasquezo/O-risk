from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.product_repository import ProductRepository
from application.use_case.manage_product import (
    create_product_service,
    get_product_service,
    get_all_products_services,
    update_product_service,
    delete_product_service
)

router = APIRouter()

class ProductServiceCreate(BaseModel):
    description: str

class ProductServiceResponse(BaseModel):
    id: int
    description: str

@router.post("/products/", response_model=ProductServiceResponse)
async def create_product(product: ProductServiceCreate, db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    created_product = await create_product_service(product,repository)
    return ProductServiceResponse(id=created_product.id, description=created_product.description)

@router.get("/products/{product_id}", response_model=ProductServiceResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    product_service = await get_product_service(product_id, repository)
    if product_service is None:
        raise HTTPException(status_code=404, detail="Product_Service not found")
    return ProductServiceResponse(id=product_service.id, description=product_service.description)

@router.get("/products/", response_model=List[ProductServiceResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    products_services = await get_all_products_services(repository)
    return [ProductServiceResponse(id=ps.id, description=ps.description) for ps in products_services]

@router.put("/products_services/{product_service_id}", response_model=ProductServiceResponse)
async def update_product(product_id: int, product_service: ProductServiceCreate, db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    updated_product = await update_product_service(product_id, product_service, repository)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product_Service not found")
    return ProductServiceResponse(id=updated_product.id, description=updated_product.description)

@router.delete("/products_services/{product_service_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    await delete_product_service(product_id, repository)
    return {"detail": "Product_Service deleted"}