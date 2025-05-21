from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.enum.UserEnum import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    otp = relationship("Otp", back_populates="user", uselist=False)
    refresh_token = relationship("RefreshToken", back_populates="user", uselist=False)


class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)
    otp = Column(Integer, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="otp")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    refresh_token = Column(String(512), nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="refresh_token")