# from pydantic import BaseModel
# from datetime import datetime

# class MessageCreate(BaseModel):
#     conversation_id: int
#     sender_id: int
#     receiver_id: int
#     content: str

# class MessageOut(BaseModel):
#     id: int
#     conversation_id: int
#     sender_id: int
#     receiver_id: int
#     content: str
#     created_at: datetime

#     class Config:
#         from_attributes = True

from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    conversation_id: int
    sender_id: int
    receiver_id: int
    content: str

class MessageResponse(MessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # dùng Pydantic v2 thay vì orm_mode
