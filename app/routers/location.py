from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.location import LocationUpdate
from app.core.database import get_db
from app.core.redis_client import redis_client
from app.crud import location as crud_location

router = APIRouter()

@router.post("/users/location")
async def update_location(data: LocationUpdate, db: AsyncSession = Depends(get_db)):
    redis_client.geoadd("user_locations", (data.lng, data.lat, str(data.user_id)))
    await crud_location.upsert_user_location(db, data.user_id, data.lat, data.lng)
    return {"message": "Đã cập nhật vị trí"}

@router.get("/users/nearby")
async def get_nearby_users(user_id: int, radius_km: float = 10, db: AsyncSession = Depends(get_db)):
    pos = redis_client.geopos("user_locations", str(user_id))
    if not pos or pos[0] is None:
        return {"message": "Không tìm thấy vị trí người dùng"}

    lng, lat = pos[0]

    nearby_ids = redis_client.geosearch(
        "user_locations",
        longitude=lng,
        latitude=lat,
        radius=radius_km,
        unit="km",
        count=100
    )
    nearby_ids = [int(uid) for uid in nearby_ids if int(uid) != user_id]

    result = await crud_location.get_nearby_user_profiles(db, nearby_ids)
    return {"nearby_users": [dict(row) for row in result]}
