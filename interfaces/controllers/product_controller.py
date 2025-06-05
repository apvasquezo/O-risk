from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.product_repository import ProductRepository
from application.use_case.manage_product import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product
)
from utils.auth import role_required

router = APIRouter(
    prefix="/products",
    tags=["Productos y Servicios"],
    #dependencies=[Depends(role_required("super"))] 
)

class ProductServiceCreate(BaseModel):
    description: str

class ProductServiceResponse(BaseModel):
    id_product: int
    description: str


@router.post("/", response_model=ProductServiceResponse, status_code=201)
async def create_product_endpoint(product: ProductServiceCreate, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ProductRepository(db)
    created = await create_product(product, repository)
    return ProductServiceResponse(**created.model_dump())

@router.get("/{product_id}", response_model=ProductServiceResponse)
async def get_product_endpoint(product_id: int, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ProductRepository(db)
    product = await get_product(product_id, repository)
    if not product:
        raise HTTPException(status_code=404, detail="Producto o servicio no encontrado")
    return ProductServiceResponse(**product.model_dump())

@router.get("/", response_model=List[ProductServiceResponse])
async def read_all_products(db: AsyncSession = Depends(get_async_session)):
    repository = ProductRepository(db)
    products = await get_all_products(repository)
    return [ProductServiceResponse(**p.model_dump()) for p in products]

@router.put("/{product_id}", response_model=ProductServiceResponse)
async def update_product_endpoint(product_id: int, product: ProductServiceCreate, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ProductRepository(db)
    updated = await update_product(product_id, product, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto o servicio no encontrado")
    return ProductServiceResponse(**updated.model_dump())

@router.delete("/{product_id}", response_model=dict)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ProductRepository(db)
    await delete_product(product_id, repository)
    return {"detail": "Producto o servicio eliminado"}
