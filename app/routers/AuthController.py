from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session

from app.schemas.UserSchema import SendOtpRequest, VerifyOtpRequest, AuthResponse, UserCreate
from app.crud import AuthService
from app.core.database import get_db
from app.models.UserModel import User
from app.security.AuthDependency import require_role

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: SendOtpRequest, db: Session = Depends(get_db)):
    await AuthService.send_otp_email(request, db)
    return {"message": "OTP has been sent to your email."}

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(user, db)

@router.post("/login", response_model=AuthResponse)
def verify_otp_and_login(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    return AuthService.verify_otp_and_login(request, db)


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return AuthService.refresh_access_token(refresh_token, db)

@router.get("/admin-test")
async def admin_only(user: User = Depends(require_role("ADMIN"))):
    return {"message": f"Welcome Admin {user.username}!"}