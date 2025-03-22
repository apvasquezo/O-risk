from sqlalchemy.orm import Session
from infrastructure.orm.models import Role

class SqlAchemyRoleRepository:
    def __init__(self, db:Session):
        self.db = db

    def create_role(self, role:Role):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_role(self, role_id:int):
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_all_roles(self):
        return self.db.query(Role).all()
    
    def update_role(self, role:Role):
        db_role = self.db.query(Role).filter(Role.id == role.id).first()
        db_role.name = role.name
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
    
    def delete_role(self, role_id:int):
        db_role = self.db.query(Role).filter(Role.id == role_id).first()
        self.db.delete(db_role)
        self.db.commit()
        return {"detail": "Role deleted successfully"}