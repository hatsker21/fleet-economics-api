from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.user import User
from src.models.vehicle import Vehicle
from src.schemas.vehicle import VehicleCreate, VehicleResponse
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Перевіряємо, чи немає вже авто з таким номером (навіть в інших компаніях)
    existing_vehicle = db.query(Vehicle).filter(Vehicle.license_plate == vehicle_in.license_plate).first()
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Автомобіль з таким номерним знаком вже зареєстровано"
        )

    # Створюємо авто, жорстко прив'язуючи його до компанії поточного юзера
    new_vehicle = Vehicle(
        **vehicle_in.model_dump(),
        company_id=current_user.company_id
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    
    return new_vehicle

@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Юзер отримує ТІЛЬКИ автомобілі своєї компанії
    vehicles = db.query(Vehicle).filter(
        Vehicle.company_id == current_user.company_id,
        Vehicle.deleted_at == None
    ).offset(skip).limit(limit).all()
    
    return vehicles