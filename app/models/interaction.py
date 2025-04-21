from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("profiles.id"))  # Người swipe
    profileId = Column(Integer, ForeignKey("profiles.id"))  # Người bị swipe
    isLike = Column(Boolean, nullable=False)  # 1 là like, 0 là dislike
    createdAt = Column(TIMESTAMP, default=datetime.utcnow)
    updatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("Profile", foreign_keys=[userId])
    profile = relationship("Profile", foreign_keys=[profileId])

