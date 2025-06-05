from pydantic import BaseModel, EmailStr
from typing import Optional

class AccountRegister(BaseModel):
    email: EmailStr


class SendOtpRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: int


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    account_id: int
    profile_id: Optional[int] = None