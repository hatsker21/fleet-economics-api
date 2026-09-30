from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.user import User, UserRole
from src.models.trip import Trip
from src.models.vehicle import Vehicle
from src.schemas.trip import TripCreate, TripResponse
from src.api.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    # 🔴 Тільки Адмін та Диспетчер планують рейси
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.DISPATCHER]))
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip_in.vehicle_id,
        Vehicle.company_id == current_user.company_id,
        Vehicle.deleted_at == None
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Автомобіль не знайдено")

    # 🟠 Перевірка бізнес-логіки: місткість
    if trip_in.passengers_carried > vehicle.passenger_capacity:
        raise HTTPException(
            status_code=400, 
            detail=f"Кількість пасажирів ({trip_in.passengers_carried}) перевищує місткість авто ({vehicle.passenger_capacity})"
        )

    driver = db.query(User).filter(
        User.id == trip_in.driver_id,
        User.company_id == current_user.company_id,
        User.role == UserRole.DRIVER,  # 🟠 Диспетчера не можна призначити за кермо
        User.deleted_at == None
    ).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Водія не знайдено у вашій компанії")

    new_trip = Trip(**trip_in.model_dump(), company_id=current_user.company_id)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

@router.get("/", response_model=List[TripResponse])
def get_trips(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Базовий запит для всіх
    query = db.query(Trip).filter(
        Trip.company_id == current_user.company_id,
        Trip.deleted_at == None
    )
    
    # 🔴 Водій бачить ТІЛЬКИ свої рейси
    if current_user.role == UserRole.DRIVER:
        query = query.filter(Trip.driver_id == current_user.id)
        
    return query.offset(skip).limit(limit).all()