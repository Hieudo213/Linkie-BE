from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationOut(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[str]
    link: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
