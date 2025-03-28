from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    func,
    Text,
    Numeric,
    DateTime
)
from sqlalchemy.orm import relationship
from ..database.db_config import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state=Column(bool, nullable=False)
    users = relationship("User", back_populates="role")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users") 
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Cause(Base):
    __tablename__ = 'causes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    risk_factor_id = Column(Integer, ForeignKey('risk_factors.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class Control(Base):
    __tablename__ = 'controls'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    control_type_id = Column(Integer, ForeignKey('risk_control_types.id'), nullable=False)
    description = Column(String(255), nullable=False)
    frequency = Column(String(100), nullable=True)
    responsible_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    risk_type_id = Column(Integer, ForeignKey('risk_types.id'), nullable=False)
    factor = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    probability_id = Column(Integer, ForeignKey('probability.id'), nullable=False)
    impact_id = Column(Integer, ForeignKey('impact.id'), nullable=False)

class EventLog(Base):
    __tablename__ = 'event_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events'), nullable=True)
    descripcion=Column(String(250), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    discovery_date = Column(DateTime, nullable=True)
    accounting_date = Column(DateTime, nullable=True)
    amount = Column(Numeric(10, 2), nullable=True)
    recovered_amount = Column(Numeric(10, 2), nullable=True)
    insurance_recovery = Column(Numeric(10, 2), nullable=True)
    risk_factor_id = Column(Integer, ForeignKey('risk_factors.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products_services.id'), nullable=True)
    process_id = Column(Integer, ForeignKey('processes.id'), nullable=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    city = Column(String(100), nullable=True)
    responsible_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(String(50), nullable=True)

class Impact(Base):
    __tablename__ = 'impact'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    definition = Column(Text)
    criteria_smlv = Column(Numeric(10, 2))

class Macroprocess(Base):
    __tablename__ = "macroprocesses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class Personal(Base):
    __tablename__ = 'personal'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    area = Column(String(100), nullable=True)
    process_id = Column(Integer, ForeignKey('processes.id'), nullable=True)
    email = Column(String(255), nullable=True)

class Probability(Base):
    __tablename__ = 'probability'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    definition = Column(Text)
    criteria_smlv = Column(Numeric(5, 2))

class Process(Base):
    __tablename__ = "processes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    macroprocess_id = Column(Integer, ForeignKey('macroprocesses.id'), nullable=False)
    description = Column(String(255), nullable=False)

class Product(Base):
    __tablename__ = "products_services"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class RiskControlType(Base):
    __tablename__ = "risk_control_types"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class RiskFactor(Base):
    __tablename__ = "risk_factors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    risk_type_id = Column(Integer, ForeignKey('risk_types.id'), nullable=False)
    description = Column(String(255), nullable=False)

class RiskType(Base):
    __tablename__ = "risk_types"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('risk_categories.id'), nullable=False)
    description = Column(String(255), nullable=False)

class Tracking(Base):
    __tablename__ = 'tracking'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    control_id = Column(Integer, ForeignKey('controls.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('event_logs.id'), nullable=False)
    tracking_date = Column(DateTime, nullable=False)
    
class Notification(Base):
    __tablename__ = 'notification'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message= Column(String(255), nullable=False)
    suggestion_control = Column(String(255), nullable=False)
    date_send = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    eventlog_id=Column(Integer, ForeignKey('event_logs.id'), nullable=False)

class History(Base):
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    eventlog_id=Column(Integer, ForeignKey('event_logs.id'), nullable=False)
    control_id = Column(Integer, ForeignKey('controls.id'), nullable=False)
    star_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    value_risk = Column(Numeric(5, 2))
