from typing import List, Optional
from domain.entities.Product import Product
from domain.repositories.product_repository import ProductRepository

async def create_product_service(description: str, repository: ProductRepository) -> Product:
    product_service = Product(description=description)
    return await repository.create_product_service(product_service)

async def get_product_service(product_service_id: int, repository: ProductRepository) -> Optional[Product]:
    return await repository.get_product_service(product_service_id)

async def get_all_products_services(repository: ProductRepository) -> List[Product]:
    return await repository.get_all_products_services()

async def update_product_service(product_service_id: int, description: str, repository: ProductRepository) -> Optional[Product]:
    product_service = Product(id=product_service_id, description=description)
    return await repository.update_product_service(product_service)

async def delete_product_service(product_service_id: int, repository: ProductRepository) -> None:
    await repository.delete_product_service(product_service_id)