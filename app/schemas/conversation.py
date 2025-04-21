from pydantic import BaseModel
from datetime import datetime

class ConversationBase(BaseModel):
    user1: int
    user2: int

class ConversationOut(ConversationBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
