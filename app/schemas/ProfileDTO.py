# app/schemas/user.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from app.enum.ProfileEnum import GenderEnum
from app.schemas.ImagesDTO import ImageOut
class ProfileOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    hobby: Optional[str] = None
    gender: GenderEnum 
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    created_at: datetime
    images: List[ImageOut]

    class Config:
        orm_mode = True

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    gender: GenderEnum
    hobby: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    
    model_config = {
       "from_attributes" : True 
    }
        