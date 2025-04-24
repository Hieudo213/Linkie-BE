from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationSchema(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[str] = None
    link: Optional[str] = None 
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True
