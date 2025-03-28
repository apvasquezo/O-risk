from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from typing import List, Optional
from domain.entities.Product import Product as ProductEntity
from infrastructure.orm.models import Product as ORMProductService

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: ProductEntity) -> ProductEntity:
        stmt = insert(ORMProductService).values(description=product.description).returning(ORMProductService.id, ORMProductService.description)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ProductEntity(id=row.id, description=row.description)

    async def get_product(self, product_id: int) -> Optional[ProductEntity]:
        stmt = select(ORMProductService).where(ORMProductService.id == product_id)
        result = await self.session.execute(stmt)
        orm_product = result.scalar_one_or_none()
        if orm_product:
            return ProductEntity(id=orm_product.id, description=orm_product.description)
        return None

    async def get_all_products(self) -> List[ProductEntity]:
        stmt = select(ORMProductService)
        result = await self.session.execute(stmt)
        orm_product = result.scalars().all()
        return [ProductEntity(id=ps.id, description=ps.description) for ps in orm_product]

    async def update_product(self, product_id: int, product: ProductEntity) -> Optional[ProductEntity]:
        stmt = update(ORMProductService).where(ORMProductService.id == product_id).values(description=product.description).returning(ORMProductService.id, ORMProductService.description)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ProductEntity(id=row.id, description=row.description)
        return None

    async def delete_product(self, product_id: int) -> None:
        stmt = delete(ORMProductService).where(ORMProductService.id == product_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Product_Service with id {product_id} not found")