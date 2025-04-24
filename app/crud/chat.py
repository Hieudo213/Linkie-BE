from sqlalchemy.orm import Session
from app.models.chat import Message
from app.schemas.chat import MessageCreate

def create_message(db: Session, msg: MessageCreate):
    db_msg = Message(**msg.dict())
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.chat import Message
# from app.schemas.chat import MessageCreate
# from datetime import datetime

# async def create_message(db: AsyncSession, msg: MessageCreate):
#     db_msg = Message(
#         conversation_id=msg.conversation_id,
#         sender_id=msg.sender_id,
#         receiver_id=msg.receiver_id,
#         content=msg.content,
#         created_at=datetime.utcnow()
#     )
#     db.add(db_msg)
#     await db.commit()
#     await db.refresh(db_msg)
#     return db_msg
