from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.LocationService import LocationService

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)

@router.post("/update_location/{account_id}")
def update_location(account_id: int, latitude: float, longitude: float, db: Session = Depends(get_db)):
    # Gọi service để cập nhật vị trí
    location = LocationService.update_location(account_id, latitude, longitude, db)

    if not location:
        raise HTTPException(status_code=404, detail="Account not found")

        # Chuyển đổi đối tượng SQLAlchemy thành dictionary để trả về
    return {"location": {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "last_updated": location.last_updated
    }}


@router.get("/nearby_users")
def get_nearby_users(current_lat: float, current_lon: float, db: Session = Depends(get_db), radius: int = 10):
    # Gọi service để tìm người dùng xung quanh
    nearby_users = LocationService.find_nearby_users(current_lat, current_lon, db, radius)

    if not nearby_users:
        raise HTTPException(status_code=404, detail="No users found in your area.")

    return {"nearby_users": [{"id": account.id,"email": account.email} for account in nearby_users]}

@router.get("/get_location_name")
def get_location_name(latitude: float, longitude: float):
    return LocationService.get_location_name(latitude, longitude);
