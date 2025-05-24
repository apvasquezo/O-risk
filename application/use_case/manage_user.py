from domain.entities.User import User
from domain.repositories.user_repository import UserRepository

async def create_user(username: str, password: str, role_id: int, repository: UserRepository):
    user = User(username=username, password=password, role_id=role_id)
    return await repository.create_user(user)

async def get_user(user_id: int, repository: UserRepository):
    return await repository.get_user(user_id)

async def get_user_username(user_name: str, repository: UserRepository):
    return await repository.get_user_username(user_name)

async def get_all_users(repository: UserRepository):
    return await repository.get_all_users()

async def update_user(user_id: int, username: str, password: str, role_id: int, repository: UserRepository):
    user = User(id_user=user_id, username=username, password=password, role_id=role_id)
    return await repository.update_user(user_id, user)

async def delete_user(user_id: int, repository: UserRepository):
    return await repository.delete_user(user_id)