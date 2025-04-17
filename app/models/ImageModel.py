from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    alt = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
