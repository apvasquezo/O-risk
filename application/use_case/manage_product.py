from typing import List, Optional
from domain.entities.Product import Product
from domain.repositories.product_repository import ProductRepository

async def create_product(product_data: Product, repository: ProductRepository) -> Product:
    return await repository.create_product(product_data)

async def get_product(product_service_id: int, repository: ProductRepository) -> Product:
    return await repository.get_product(product_service_id)

async def get_all_products(repository: ProductRepository) -> List[Product]:
    return await repository.get_all_products()

async def update_product(product_service_id: int, product_data: Product, repository: ProductRepository) -> Product:
    return await repository.update_product(product_service_id, product_data)

async def delete_product(product_service_id: int, repository: ProductRepository) -> None:
    await repository.delete_product(product_service_id)