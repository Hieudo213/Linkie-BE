from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("profiles.id"))
    receiver_id = Column(Integer, ForeignKey("profiles.id"))
    content = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # conversation = relationship("Conversation")

    conversation = relationship("Conversation", back_populates="messages")