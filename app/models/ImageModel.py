from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    alt = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)

    # 👉 Khoá ngoại trỏ đến bảng profile
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    # Optional: relationship ngược lại (nếu bạn cần đi từ Image → Profile)
    profile = relationship("Profile", back_populates="images")
