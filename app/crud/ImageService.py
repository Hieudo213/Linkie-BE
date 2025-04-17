import os
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.models.ImageModel import Image

class ImageService:
    @staticmethod
    def upload_image(file: UploadFile, db: Session) -> Image:
        if not file:
            raise HTTPException(status_code=400, detail="File must not be empty")

        # Tạo thư mục nếu chưa có
        save_dir = os.path.join(os.getcwd(), "Images")
        os.makedirs(save_dir, exist_ok=True)

        # Đường dẫn lưu file
        save_path = os.path.join(save_dir, file.filename)

        # Lưu file vào ổ đĩa
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Tạo entity Image
        image_data = Image(
            title=file.filename,
            url=save_path,
            alt=os.path.splitext(file.filename)[0],
            upload_date=datetime.utcnow()
        )

        # Lưu vào DB
        db.add(image_data)
        db.commit()
        db.refresh(image_data)

        return image_data

    @staticmethod
    def get_image_by_id(id: int, db: Session) -> FileResponse:
        # 1. Truy vấn ảnh từ DB
        image = db.query(Image).filter(Image.id == id).first()

        if not image:
            raise HTTPException(status_code=404, detail=f"Image with ID {id} not found in the database")

        # 2. Kiểm tra đường dẫn file có tồn tại không
        image_path = image.url  # Đường dẫn lưu trong DB

        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image file not found on server")

        # 3. Trả file như tài nguyên
        return FileResponse(path=image_path, media_type="image/jpeg", filename=image.title)

    def delete_image_by_id(id: int, db: Session):
        # 1. Truy vấn ảnh trong DB
        image = db.query(Image).filter(Image.id == id).first()

        if not image:
            raise HTTPException(status_code=404, detail=f"Image with ID {id} not found")

        # 2. Xoá file trên ổ đĩa nếu tồn tại
        image_path = image.url
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print(f"⚠️ File không tồn tại tại {image_path}, chỉ xoá bản ghi DB")

        # 3. Xoá bản ghi khỏi DB
        db.delete(image)
        db.commit()