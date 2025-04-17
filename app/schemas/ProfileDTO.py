# app/schemas/user.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.enum.ProfileEnum import GenderEnum
class ProfileOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    hobby: Optional[str] = None
    gender: GenderEnum 
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    created_at: datetime

    model_config = {
       "from_attributes" : True 
    }

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
        