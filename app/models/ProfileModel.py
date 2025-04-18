from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.enum.ProfileEnum import GenderEnum, HobbyEnum
from app.core.base import Base
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)
    hobby = Column(Enum(HobbyEnum))
    gender = Column(Enum(GenderEnum), nullable=False)
    date_of_birth = Column(Date)
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 👉 Quan hệ 1-N: Một profile có nhiều ảnh
    images = relationship("Image", back_populates="profile", cascade="all, delete-orphan")