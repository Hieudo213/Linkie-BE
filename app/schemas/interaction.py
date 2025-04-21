from pydantic import BaseModel
from datetime import datetime

class InteractionBase(BaseModel):
    userId: int
    profileId: int
    isLike: bool

class InteractionCreate(InteractionBase):
    pass

class InteractionOut(InteractionBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
