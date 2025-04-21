from pydantic import BaseModel

class LocationUpdate(BaseModel):
    user_id: int
    lat: float
    lng: float
