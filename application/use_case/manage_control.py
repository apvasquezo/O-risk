from domain.entities.Control import Control
from domain.repositories.control_repository import ControlRepository

async def create_control(control_data: Control, repository: ControlRepository) -> Control:
    return await repository.create_control(control_data)

async def get_control(control_id: int, repository: ControlRepository) -> Control:
    return await repository.get_control(control_id)

async def get_all_controls(repository: ControlRepository) -> list[Control]:
    return await repository.get_all_controls()

async def update_control(control_id: int, control_data: Control, repository: ControlRepository) -> Control:
    return await repository.update_control(control_id, control_data)

async def delete_control(control_id: int, repository: ControlRepository) -> None:
    await repository.delete_control(control_id)