from fastapi import HTTPException
from sqlalchemy import String
from sqlalchemy.orm import Session

from app.models.ProfileModel import Profile
from app.models.ImageModel import AccountAvatar
from app.models.UserModel import Account, Otp, RefreshToken


def delete_account_no_constraint_by_email_service(email: str, db: Session) -> String:
    account = db.query(Account).filter(Account.email == email).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Nếu tồn tại bất kỳ liên kết nào → KHÔNG xoá
    linked_tables = []

    if db.query(Otp).filter(Otp.account_id == account.id).first():
        linked_tables.append("Otp")

    if db.query(RefreshToken).filter(RefreshToken.account_id == account.id).first():
        linked_tables.append("RefreshToken")

    if db.query(Profile).filter(Profile.account_id == account.id).first():
        linked_tables.append("Profile")

    if db.query(AccountAvatar).filter(AccountAvatar.account_id == account.id).first():
        linked_tables.append("AccountAvatar")

    if linked_tables:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete account. Linked records exist in: {', '.join(linked_tables)}"
        )

    # Nếu không bị liên kết → xoá bình thường
    db.delete(account)
    db.commit()
    return f"Account with ID {email} deleted successfully"


def delete_account_with_otp_constraint(email: str, db: Session) -> String:
    account = db.query(Account).filter(Account.email == email).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account_id = account.id

    # Xoá OTP nếu có
    otp = db.query(Otp).filter(Otp.account_id == account_id).first()
    if otp:
        db.delete(otp)

    # Cuối cùng xoá Account
    db.delete(account)
    db.commit()

    return f"Account with email '{email}' and related records deleted successfully."