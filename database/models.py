# database/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    status = Column(String(50), default="draft")
    variants = Column(JSON)  # Lista de variantes
    metrics = Column(JSON)   # Métricas a serem rastreadas
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

class UserAssignment(Base):
    __tablename__ = "user_assignments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    experiment_id = Column(Integer, nullable=False)
    variant = Column(String(100), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    experiment_id = Column(Integer, nullable=False)
    event_type = Column(String(100), nullable=False)  # 'conversion', 'click', etc.
    event_value = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)