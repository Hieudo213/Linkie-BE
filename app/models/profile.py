# app/models/user.py
from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

# Định nghĩa Base
Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    gender = Column(String, nullable=False)
    date_of_birth = Column(Date)
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())