from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.enum.UserEnum import UserRole

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_activated = Column(Boolean, default=False)
    otp = relationship("Otp", back_populates="account", uselist=False)
    refresh_token = relationship("RefreshToken", back_populates="account", uselist=False)

    # One-to-one với AccountAvatar
    avatar = relationship("AccountAvatar", back_populates="account", uselist=False, cascade="all, delete")
    profile = relationship("Profile", back_populates="account", uselist=False, cascade="all, delete")
    location = relationship("UserLocation", uselist=False, backref="account")

class Otp(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True)
    otp = Column(Integer, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    account = relationship("Account", back_populates="otp")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True)
    refresh_token = Column(String(512), nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    account = relationship("Account", back_populates="refresh_token")
