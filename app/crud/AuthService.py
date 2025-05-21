import random
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.UserModel import User, Otp, RefreshToken
from app.schemas.UserSchema import SendOtpRequest, VerifyOtpRequest, AuthResponse, UserCreate
from app.crud.EmailService import EmailService
from app.security.JwtService import JwtService


email_service = EmailService()
jwt_service = JwtService()


def generate_otp_code() -> int:
    return random.randint(100000, 999999)


async def send_otp_email(request: SendOtpRequest, db: Session):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist")

    existing_otp = db.query(Otp).filter(Otp.user_id == user.id).first()
    now = datetime.utcnow()

    if existing_otp:
        if existing_otp.expiration_time > now:
            raise HTTPException(status_code=400, detail="OTP already sent. Please wait before requesting another.")
        db.delete(existing_otp)
        db.commit()

    otp_code = generate_otp_code()
    expires_at = now + timedelta(minutes=2)

    otp = Otp(
        user_id=user.id,
        otp=otp_code,
        expiration_time=expires_at
    )
    db.add(otp)
    db.commit()

    # Gửi email
    import asyncio
    asyncio.create_task(email_service.send_email_otp(email=user.email, otp=otp_code))


def verify_otp_and_login(request: VerifyOtpRequest, db: Session) -> AuthResponse:
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_entry = db.query(Otp).filter(Otp.user_id == user.id, Otp.otp == request.otp).first()
    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expiration_time < datetime.utcnow():
        db.delete(otp_entry)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    # OTP is valid → delete it
    db.delete(otp_entry)
    db.commit()

    # Access & Refresh Token
    access_token = jwt_service.create_access_token(subject=user.email)
    refresh_token_str = jwt_service.create_refresh_token(subject=user.email)

    # Lưu refresh token vào DB (nếu chưa có thì tạo mới, nếu có thì cập nhật)
    refresh = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
    expires_at = datetime.utcnow() + timedelta(hours=jwt_service.refresh_token_expire_hours)

    if refresh:
        refresh.refresh_token = refresh_token_str
        refresh.expiration_time = expires_at
    else:
        refresh = RefreshToken(
            user_id=user.id,
            refresh_token=refresh_token_str,
            expiration_time=expires_at
        )
        db.add(refresh)

    db.commit()

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token_str
    )

def register_user(user_data: UserCreate, db: Session):
    # Kiểm tra email hoặc username đã tồn tại
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        role="USER"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully!"}


def refresh_access_token(refresh_token: str, db: Session) -> AuthResponse:
    token_record = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_record.expiration_time < datetime.utcnow():
        db.delete(token_record)
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = token_record.user

    new_access_token = jwt_service.create_access_token(subject=user.email)
    return AuthResponse(
        access_token=new_access_token,
        refresh_token=token_record.refresh_token
    )
