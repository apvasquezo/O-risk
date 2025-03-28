from domain.entities.User import User
from infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository

def create_user(username: str, password: str, role_id: int, repository: SqlAlchemyUserRepository):
    user = User(username=username, password=password, role_id=role_id)
    return repository.create_user(user)

def get_user(user_id: int, repository: SqlAlchemyUserRepository):
    return repository.get_user(user_id)

def get_all_users(repository: SqlAlchemyUserRepository):
    return repository.get_all_users()

def update_user(user_id: int, username: str, password: str, role_id: int, repository: SqlAlchemyUserRepository):
    user = User(id=user_id, username=username, password=password, role_id=role_id)
    return repository.update_user(user)

def delete_user(user_id: int, repository: SqlAlchemyUserRepository):
    return repository.delete_user(user_id)