# app/schemas/user.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from app.enum.ProfileEnum import GenderEnum, HobbyEnum
from app.schemas.ImagesDTO import ImageOut
class ProfileOut(BaseModel):
    id: int
    username: str
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    created_at: datetime
    images: List[ImageOut]
    target_type: Optional[str] = None
    hobby: Optional[List[HobbyEnum]] = None

    class Config:
        orm_mode = True

class ProfileCreate(BaseModel):
    username: str
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    target_type: Optional[str] = None
    hobby: Optional[List[HobbyEnum]] = None
    
    model_config = {
       "from_attributes" : True 
    }
        