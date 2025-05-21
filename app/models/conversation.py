from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    user1 = Column(Integer, ForeignKey("profiles.id"))
    user2 = Column(Integer, ForeignKey("profiles.id"))
    createdAt = Column(TIMESTAMP, default=datetime.utcnow)
    updatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_one = relationship("Profile", foreign_keys=[user1])
    user_two = relationship("Profile", foreign_keys=[user2])

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")