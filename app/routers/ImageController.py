from typing import List

from fastapi import UploadFile, File, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.ImageService import ImageService

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/account/{account_id}")
def upload_avatar_account_endpoint(account_id: int, file: UploadFile, db: Session = Depends(get_db)):
    image = ImageService.upload_account_avatar_image(file, db, account_id)
    return {"image": image}

@router.get("/account/{image_id}")
def get_account_avatar_endpoint(image_id: int, db: Session = Depends(get_db)):
    try:
        # Gọi hàm trong ImageService để lấy avatar
        return ImageService.get_account_avatar_by_id(image_id, db)
    except HTTPException as e:
        # Trả lỗi nếu có vấn đề
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/account{image_id}")
def delete_account_avatar_endpoint(image_id: int, db: Session = Depends(get_db)):
    ImageService.delete_account_avatar_by_id(image_id, db)
    return {"message": f"Image with ID {image_id} deleted successfully (file + database)"}

@router.post("/profile/{profile_id}")
def upload_profile_images_endpoint(profile_id: int, files: List[UploadFile], db: Session = Depends(get_db)):
    uploaded_images = ImageService.upload_profile_images(files, db, profile_id)
    return {"uploaded_images": uploaded_images}

@router.get("/profile/{image_id}")
def get_profile_images_endpoint(image_id: int, db: Session = Depends(get_db)):
    try:
        # Gọi hàm trong ImageService để lấy avatar
        return ImageService.get_profile_images_by_id(image_id, db)
    except HTTPException as e:
        # Trả lỗi nếu có vấn đề
        raise HTTPException(status_code=e.status_code, detail=e.detail)
