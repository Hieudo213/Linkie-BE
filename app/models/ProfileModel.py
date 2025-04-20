from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Enum, ARRAY
from sqlalchemy.sql import func
from app.enum.ProfileEnum import GenderEnum, HobbyEnum
from app.core.base import Base
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column((Enum(GenderEnum)), nullable=False)
    date_of_birth = Column(Date)
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    target_type = Column(String(1000))
    hobby = Column(
        ARRAY(Enum(HobbyEnum, name="hobbyenum", validate_strings=True)),
        nullable=True
    )
    # 👉 Quan hệ 1-N: Một profile có nhiều ảnh
    images = relationship("Image", back_populates="profile", cascade="all, delete-orphan")