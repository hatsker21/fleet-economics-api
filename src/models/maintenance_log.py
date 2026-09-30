import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from src.models.base import Base

class MaintenanceType(str, enum.Enum):
    REPAIR = "repair"       # Поломка/Ремонт
    SERVICE = "service"     # Планове ТО (мастило, фільтри)
    TIRES = "tires"         # Шиномонтаж
    OTHER = "other"         # Інше

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)

    type = Column(Enum(MaintenanceType), nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)  # Вартість у копійках
    odometer = Column(Integer, nullable=False) # Пробіг на момент ремонту
    
    performed_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())