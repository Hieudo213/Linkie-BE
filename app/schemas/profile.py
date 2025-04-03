# app/schemas/user.py
from pydantic import BaseModel
from datetime import date, datetime

class ProfileOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    gender: str
    date_of_birth: date | None = None
    bio: str | None = None
    created_at: datetime

    model_config = {
       "from_attributes" : True 
    }
        