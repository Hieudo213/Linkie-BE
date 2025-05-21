from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.package import PackageCreate, PackageOut, PurchaseCreate, PurchaseOut
from app.crud.package import create_package, create_purchase, get_all_packages, update_purchase_status
from app.core.database import get_db
import uuid
from app.core.vnpay import create_vnpay_url

router = APIRouter()

@router.get("/packages", response_model=list[PackageOut])
def list_packages(db: Session = Depends(get_db)):
    return get_all_packages(db)

@router.post("/packages", response_model=PackageOut)
def add_package(data: PackageCreate, db: Session = Depends(get_db)):
    return create_package(db, data)

@router.post("/purchase", response_model=dict)
def start_purchase(data: PurchaseCreate, user_id: int, request: Request, db: Session = Depends(get_db)):
    vnp_txn_ref = str(uuid.uuid4())
    purchase = create_purchase(db, user_id, data.package_id, vnp_txn_ref)
    payment_url = create_vnpay_url(request, amount=100000, txn_ref=vnp_txn_ref)  # Tùy chỉnh giá
    return {"payment_url": payment_url}

@router.get("/payment/callback")
def vnpay_callback(vnp_TxnRef: str, vnp_TransactionNo: str, vnp_ResponseCode: str, db: Session = Depends(get_db)):
    status = "success" if vnp_ResponseCode == "00" else "failed"
    update_purchase_status(db, vnp_TxnRef, status, vnp_TransactionNo)
    return {"message": "Payment processed", "status": status}
