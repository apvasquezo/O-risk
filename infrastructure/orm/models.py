from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    func,
    Text,
    Numeric,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from ..orm.base import Base

class Role(Base):
    __tablename__ = "roles"
    
    id_role = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state=Column(Boolean, nullable=False, default=True)
    users = relationship("User", back_populates="role", lazy='joined')
    
class User(Base):
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id_role"), nullable=False)
    role = relationship("Role", back_populates="users", lazy='joined')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Cause(Base):
    __tablename__ = 'causes'
    
    id_cause = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    risk_factor_id = Column(Integer, ForeignKey('risk_factors.id_factor'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id_event'), nullable=False)

class Consequence(Base):
    __tablename__ = 'consequence'
    
    id_consequence = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    risk_factor_id = Column(Integer, ForeignKey('risk_factors.id_factor'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id_event'), nullable=False)
class Channel(Base):
    __tablename__ = "channels"
    
    id_channel = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(50), nullable=False)

class Control(Base):
    __tablename__ = 'controls'
    
    id_control = Column(Integer, primary_key=True, autoincrement=True)
    control_type_id = Column(Integer, ForeignKey('risk_control_types.id_controltype'), nullable=False)
    description = Column(String(255), nullable=False)
    frequency = Column(String(100), nullable=True)
    responsible_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=False)

class Event(Base):
    __tablename__ = 'events'
    
    id_event = Column(Integer, primary_key=True, autoincrement=True)
    risk_type_id = Column(Integer, ForeignKey('risk_types.id_risktype'), nullable=False)
    factor_id = Column(Integer, ForeignKey('risk_factors.id_factor'), nullable=True)
    description = Column(Text, nullable=False)
    probability_id = Column(Integer, ForeignKey('probability.level'), nullable=False)
    impact_id = Column(Integer, ForeignKey('impact.level'), nullable=False)

class EventLog(Base):
    __tablename__ = 'event_logs'
    
    id_eventlog = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id_event'), nullable=True)
    description=Column(String(250), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    discovery_date = Column(DateTime, nullable=True)
    accounting_date = Column(DateTime, nullable=True)
    amount = Column(Numeric(10, 2), nullable=True)
    recovered_amount = Column(Numeric(10, 2), nullable=True)
    insurance_recovery = Column(Numeric(10, 2), nullable=True)
    risk_factor_id = Column(Integer, ForeignKey('risk_factors.id_factor'), nullable=True)
    product_id = Column(Integer, ForeignKey('products_services.id_product'), nullable=True)
    process_id = Column(Integer, ForeignKey('processes.id_process'), nullable=True)
    channel_id = Column(Integer, ForeignKey('channels.id_channel'), nullable=True)
    city = Column(String(100), nullable=True)
    responsible_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=True)
    status = Column(String(50), nullable=True)

class Impact(Base):
    __tablename__ = 'impact'
    
    #id_impact = Column(Integer, autoincrement=True)
    level = Column(Integer,primary_key=True, nullable=False)
    description = Column(String(100), nullable=False)
    definition = Column(Text)
    criteria_smlv = Column(Numeric(10, 2))

class Macroprocess(Base):
    __tablename__ = "macroprocesses"
    
    id_macro = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(100), nullable=False)

class Personal(Base):
    __tablename__ = 'personal'
    
    id_personal = Column(String(15), primary_key=True) #esta debe ser la cedula del empleado
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    area = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    notify=Column(Boolean, nullable=False, default=False)

class Probability(Base):
    __tablename__ = 'probability'
    
    #id_probability = Column(Integer,  autoincrement=True)
    level = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(100), nullable=False)
    definition = Column(Text)
    criteria_por = Column(Numeric(5, 2))

class Process(Base):
    __tablename__ = "processes"
    
    id_process = Column(Integer, primary_key=True, index=True, autoincrement=True)
    macroprocess_id = Column(Integer, ForeignKey('macroprocesses.id_macro'), nullable=False)
    description = Column(String(255), nullable=False)
    personal_id= Column(String(15), ForeignKey('personal.id_personal'), nullable=False)

class Product(Base):
    __tablename__ = "products_services"
    
    id_product = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(100), nullable=False)

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    
    id_riskcategory = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)

class RiskControlType(Base):
    __tablename__ = "risk_control_types"
    
    id_controltype = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(100), nullable=False)

class RiskFactor(Base):
    __tablename__ = "risk_factors"
    
    id_factor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    risk_type_id = Column(Integer, ForeignKey('risk_types.id_risktype'), nullable=False)
    description = Column(String(255), nullable=False)

class RiskType(Base):
    __tablename__ = "risk_types"
    
    id_risktype = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('risk_categories.id_riskcategory'), nullable=False)
    description = Column(String(255), nullable=False)

class Tracking(Base):
    __tablename__ = 'tracking'
    
    id_tracking = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=False)
    control_id = Column(Integer, ForeignKey('controls.id_control'), nullable=False)
    event_id = Column(Integer, ForeignKey('event_logs.id_eventlog'), nullable=False)
    tracking_date = Column(DateTime, nullable=False)
    
class Notification(Base):
    __tablename__ = 'notification'
    
    id_notify = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(255), nullable=False)
    suggestion_control = Column(String(255), nullable=False)
    date_send = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default='pendiente')  # enviado, fallido, leído
    type = Column(String(50), default='email')  # email, push, interna
    personal_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=False)
    eventlog_id = Column(Integer, ForeignKey('event_logs.id_eventlog'), nullable=False)

class History(Base):
    __tablename__ = 'history'
    
    id_history = Column(Integer, primary_key=True, autoincrement=True)
    eventlog_id=Column(Integer, ForeignKey('event_logs.id_eventlog'), nullable=False)
    control_id = Column(Integer, ForeignKey('controls.id_control'), nullable=False)
    star_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    value_risk = Column(Numeric(5, 2))

class Plan_action(Base):
    __tablename__ = 'plan_action'
    
    id_plan = Column(Integer, primary_key=True, autoincrement=True)
    description=Column(String(255), nullable=False)
    star_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    personal_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=False)
    state=Column(String(50), nullable=True)
    
class Control_action(Base):
    __tablename__ = 'control_action'
    id_controlaction=Column(Integer, primary_key=True, autoincrement=True)
    control_id=Column(Integer, ForeignKey('controls.id_control'), nullable=False)
    action_id=Column(Integer, ForeignKey('plan_action.id_plan'), nullable=False)
    
class Evaluation(Base):
    __tablename__ = 'evaluation_control'
    
    id_evaluation = Column(Integer, primary_key=True, autoincrement=True)
    control_id=Column(Integer, ForeignKey('controls.id_control'), nullable=False)
    event_id=Column(Integer, ForeignKey('events.id_event'), nullable=False)
    eval_date=Column(DateTime, nullable=False)
    n_probability=Column(Integer, ForeignKey('probability.level'), nullable=False)
    n_impact=Column(Integer, ForeignKey('impact.level'), nullable=False)
    personal_id = Column(String(15), ForeignKey('personal.id_personal'), nullable=False)
    next_date = Column(DateTime, nullable=False)
    description=Column(String(255), nullable=False)
    state=Column(String(50), nullable=True)
    
class Alert(Base):
    __tablename__ = 'alert'

    id_alert = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)  # Breve título de la alerta
    message = Column(String(255), nullable=False)  # Contenido de la alerta
    is_read = Column(Boolean, default=False)  # Indicador si ya fue leída
    date_created = Column(DateTime, nullable=False)  # Fecha de creación
    role_id = Column(String(50), nullable=False)  # Rol objetivo que verá la alerta (ej. 'Administrador', 'Supervisor')
    type = Column(String(50), nullable=False)  # Tipo de alerta: 'evento', 'control', etc.
    eventlog_id = Column(Integer, ForeignKey('event_logs.id_eventlog'), nullable=True)
    #eventlog = relationship("EventLog",  back_populates="alert", lazy='joined')
    control_id = Column(Integer, ForeignKey('controls.id_control'), nullable=True)