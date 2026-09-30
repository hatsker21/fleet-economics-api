from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.user import User
from src.models.trip import Trip
from src.models.vehicle import Vehicle
from src.schemas.trip import TripCreate, TripResponse
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Перевіряємо, чи належить автомобіль компанії поточного користувача
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip_in.vehicle_id,
        Vehicle.company_id == current_user.company_id,
        Vehicle.deleted_at == None
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автомобіль не знайдено у вашому автопарку"
        )

    # 2. Перевіряємо, чи належить водій до цієї ж компанії
    driver = db.query(User).filter(
        User.id == trip_in.driver_id,
        User.company_id == current_user.company_id,
        User.deleted_at == None
    ).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Водія не знайдено у вашій компанії"
        )

    # Створюємо рейс
    new_trip = Trip(
        **trip_in.model_dump(),
        company_id=current_user.company_id
    )
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
    trips = db.query(Trip).filter(
        Trip.company_id == current_user.company_id,
        Trip.deleted_at == None
    ).offset(skip).limit(limit).all()
    
    return trips