from domain.entities.User import User
from infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from domain.repositories.user_repository import UserRepository

async def create_user(username: str, password: str, role_id: int, repository: UserRepository):
    user = User(username=username, password=password, role_id=role_id)
    return await repository.create_user(user)

def get_user(user_id: int, repository: UserRepository):
    return repository.get_user(user_id)

async def get_user_username(user_name: str, repository: UserRepository):
    return await repository.get_user_username(user_name)

def get_all_users(repository: UserRepository):
    return repository.get_all_users()

def update_user(user_id: int, username: str, password: str, role_id: int, repository: UserRepository):
    user = User(id_user=user_id, username=username, password=password, role_id=role_id)
    return repository.update_user(user_id, user)

def delete_user(user_id: int, repository: UserRepository):
    return repository.delete_user(user_id)