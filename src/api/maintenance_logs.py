from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.user import User, UserRole
from src.models.maintenance_log import MaintenanceLog
from src.models.vehicle import Vehicle
from src.schemas.maintenance_log import MaintenanceLogCreate, MaintenanceLogResponse
from src.api.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/maintenance-logs", tags=["Maintenance Logs"])

@router.post("/", response_model=MaintenanceLogResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_log(
    log_in: MaintenanceLogCreate,
    db: Session = Depends(get_db),
    # 🔴 Тільки Адмін та Диспетчер можуть додавати витрати на ремонт
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.DISPATCHER]))
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == log_in.vehicle_id,
        Vehicle.company_id == current_user.company_id,
        Vehicle.deleted_at == None
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Автомобіль не знайдено у вашому автопарку")

    new_log = MaintenanceLog(**log_in.model_dump(), company_id=current_user.company_id)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/", response_model=List[MaintenanceLogResponse])
def get_maintenance_logs(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(MaintenanceLog).filter(
        MaintenanceLog.company_id == current_user.company_id
    ).offset(skip).limit(limit).all()
    
    return logs