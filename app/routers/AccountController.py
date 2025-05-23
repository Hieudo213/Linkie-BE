# app/routers/account_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import String
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.AccountService import delete_account_no_constraint_by_email_service, delete_account_with_otp_constraint

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.delete("/no-constraint/{email}", status_code=status.HTTP_200_OK)
def delete_account_no_constraint_by_email(email: str, db: Session = Depends(get_db)):
    result: String = delete_account_no_constraint_by_email_service(email, db)
    return {"message": result}

@router.delete("/otp-constraint/{email}", status_code=status.HTTP_200_OK)
def delete_account_after_failed_verification(email: str, db: Session = Depends(get_db)):
    result: String = delete_account_with_otp_constraint(email, db)
    return {"message": result}