import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from src.models.base import Base

class TripStatus(str, enum.Enum):
    SCHEDULED = "scheduled"      # Заплановано
    IN_PROGRESS = "in_progress"  # В дорозі
    COMPLETED = "completed"      # Завершено
    CANCELLED = "cancelled"      # Скасовано

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    origin_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    departure_time = Column(DateTime(timezone=True), nullable=False)
    distance_km = Column(Integer, nullable=False)
    ticket_price = Column(Integer, nullable=False)  # Зберігаємо в копійках
    passengers_carried = Column(Integer, default=0)
    
    status = Column(Enum(TripStatus), default=TripStatus.SCHEDULED, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)