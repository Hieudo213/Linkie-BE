from pydantic import BaseModel
from typing import List
from datetime import datetime

class Profile(BaseModel):
    id: int
    userId: int
    profileId: int
    isLike: bool
    createdAt: datetime

class InteractionListResponse(BaseModel):
    code: str
    message: str
    profiles: List[Profile]
