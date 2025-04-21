from sqlalchemy.orm import Session
from app.models.chat import Message
from app.schemas.chat import MessageCreate

def create_message(db: Session, msg: MessageCreate):
    db_msg = Message(**msg.dict())
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg
