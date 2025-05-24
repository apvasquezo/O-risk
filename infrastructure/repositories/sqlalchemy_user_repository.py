from sqlalchemy.orm import Session
from infrastructure.orm.models import User as ORMUser
from domain.entities.User import User

class SqlAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: User):
        db_user = ORMUser(username=user.username, password=user.password, role_id=user.role_id)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(ORMUser).filter(ORMUser.id_user == user_id).first()

    def get_all_users(self):
        return self.db.query(ORMUser).all()

    def update_user(self, user: User):
        print("ya estoy en el repositorio ", user)
        db_user = self.db.query(ORMUser).filter(ORMUser.id_user == user.id).first()
        db_user.username = user.username
        db_user.password = user.password
        db_user.role_id = user.role_id
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.db.query(ORMUser).filter(ORMUser.id_user == user_id).first()
        self.db.delete(db_user)
        self.db.commit()
        return {"detail": "User deleted successfully"}