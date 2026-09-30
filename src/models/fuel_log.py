from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models.base import Base

class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    
    liters = Column(Numeric(8, 2), nullable=False)
    price_per_liter = Column(Integer, nullable=False) # в копійках
    total_cost = Column(Integer, nullable=False)      # в копійках
    
    odometer = Column(Integer, nullable=False)        # Пробіг на момент заправки
    
    refueled_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())