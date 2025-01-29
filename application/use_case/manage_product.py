from typing import List, Optional
from domain.entities.Product import Product_Service
from domain.repositories.product_repository import ProductServiceRepository

async def create_product_service(description: str, repository: ProductServiceRepository) -> Product_Service:
    product_service = Product_Service(description=description)
    return await repository.create_product_service(product_service)

async def get_product_service(product_service_id: int, repository: ProductServiceRepository) -> Optional[Product_Service]:
    return await repository.get_product_service(product_service_id)

async def get_all_products_services(repository: ProductServiceRepository) -> List[Product_Service]:
    return await repository.get_all_products_services()

async def update_product_service(product_service_id: int, description: str, repository: ProductServiceRepository) -> Optional[Product_Service]:
    product_service = Product_Service(id=product_service_id, description=description)
    return await repository.update_product_service(product_service)

async def delete_product_service(product_service_id: int, repository: ProductServiceRepository) -> None:
    await repository.delete_product_service(product_service_id)