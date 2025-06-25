import os
import shutil
from datetime import datetime
from typing import List
import mimetypes
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.models.ImageModel import AccountAvatar, ProfileImage
from app.models.ProfileModel import Profile
from app.models.UserModel import Account
from uuid import uuid4

class ImageService:
    # @staticmethod
    # def upload_account_avatar_image(file: UploadFile, db: Session, email: str) -> AccountAvatar:
    #     if not file:
    #         raise HTTPException(status_code=400, detail="File must not be empty")

    #         # Tạo thư mục nếu chưa có
    #     save_dir = os.path.join(os.getcwd(), "Images")
    #     os.makedirs(save_dir, exist_ok=True)

    #     # Đường dẫn lưu file
    #     save_path = os.path.join(save_dir, file.filename)

    #     # Lưu file vào ổ đĩa
    #     with open(save_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)

    #     # Kiểm tra account_id, đảm bảo account tồn tại
    #     account = db.query(Account).filter(Account.email == email).first()
    #     if not account:
    #         raise HTTPException(status_code=404, detail="Account not found")

    #     account_id = account.id;
    #     # Tạo entity AccountAvatar và gắn account_id vào
    #     image_data = AccountAvatar(
    #         title=file.filename,
    #         url=save_path,
    #         alt=os.path.splitext(file.filename)[0],
    #         upload_date=datetime.utcnow(),
    #         account_id=account_id  # Gắn account_id vào avatar
    #     )

    #     # Lưu vào DB
    #     db.add(image_data)
    #     db.commit()
    #     db.refresh(image_data)

    #     return image_data
    @staticmethod
    def upload_account_avatar_image(file: UploadFile, db: Session, email: str) -> AccountAvatar:
        if not file:
            raise HTTPException(status_code=400, detail="File must not be empty")

    # Tạo thư mục static/avatar nếu chưa có
        STATIC_AVATAR_DIR = os.path.join("static", "images", "avatar")
        os.makedirs(STATIC_AVATAR_DIR, exist_ok=True)

    # Tạo tên file duy nhất
        ext = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        save_path = os.path.join(STATIC_AVATAR_DIR, filename)

    # Ghi file ra ổ đĩa
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Kiểm tra account
        account = db.query(Account).filter(Account.email == email).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        image_data = AccountAvatar(
            title=filename,
            url=os.path.join("static", "images", "avatar", filename),
            alt=os.path.splitext(file.filename)[0],
            upload_date=datetime.utcnow(),
            account_id=account.id
        )

        db.add(image_data)
        db.commit()
        db.refresh(image_data)
        
        if account.profile:
           account.profile.avatar_id = image_data.id
           db.commit()
           
        return image_data


    @staticmethod
    def get_account_avatar_by_id(id: int, db: Session) -> FileResponse:
        image = db.query(AccountAvatar).filter(AccountAvatar.id == id).first()
        if not image:
            raise HTTPException(status_code=404, detail=f"Image with ID {id} not found in the database")

        image_path = os.path.join(os.getcwd(), image.url)
        if not os.path.isfile(image_path):
            raise HTTPException(status_code=404, detail="Image file not found on server")

        mime_type, _ = mimetypes.guess_type(image_path)
        return FileResponse(path=image_path, media_type=mime_type or "application/octet-stream", filename=image.title)
    
    @staticmethod
    def delete_account_avatar_by_id(id: int, db: Session):
        image = db.query(AccountAvatar).filter(AccountAvatar.id == id).first()
        if not image:
            raise HTTPException(status_code=404, detail=f"Image with ID {id} not found")

        file_path = os.path.join(os.getcwd(), image.url)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.delete(image)
        db.commit()



    # @staticmethod
    # def get_account_avatar_by_id(id: int, db: Session) -> FileResponse:
    #     # 1. Truy vấn ảnh từ DB
    #     image = db.query(AccountAvatar).filter(AccountAvatar.id == id).first()

    #     if not image:
    #         raise HTTPException(status_code=404, detail=f"Image with ID {id} not found in the database")

    #     # 2. Kiểm tra đường dẫn file có tồn tại không
    #     image_path = image.url  # Đường dẫn lưu trong DB
    #     if not os.path.exists(image_path):
    #         raise HTTPException(status_code=404, detail="Image file not found on server")

    #     # 3. Xác định loại MIME (media_type) của ảnh dựa trên phần mở rộng của file
    #     mime_type, _ = mimetypes.guess_type(image_path)
    #     if not mime_type:
    #         mime_type = "application/octet-stream"  # Mặc định nếu không xác định được loại MIME

    #     # 4. Trả file như tài nguyên
    #     return FileResponse(path=image_path, media_type=mime_type, filename=image.title)

    # @staticmethod
    # def delete_account_avatar_by_id(id: int, db: Session):
    #     # 1. Truy vấn ảnh trong DB
    #     image = db.query(AccountAvatar).filter(AccountAvatar.id == id).first()

    #     if not image:
    #         raise HTTPException(status_code=404, detail=f"Image with ID {id} not found")

    #     # 2. Xoá file trên ổ đĩa nếu tồn tại
    #     image_path = image.url
    #     if os.path.exists(image_path):
    #         os.remove(image_path)
    #     else:
    #         print(f"⚠️ File không tồn tại tại {image_path}, chỉ xoá bản ghi DB")

    #     # 3. Xoá bản ghi khỏi DB
    #     db.delete(image)
    #     db.commit()

    @staticmethod
    def upload_profile_images(files: List[UploadFile], db: Session, profile_id: int) -> List[ProfileImage]:
        # Kiểm tra số lượng ảnh (tối thiểu 2, tối đa 6 ảnh)
        if len(files) < 2 or len(files) > 6:
            raise HTTPException(status_code=400, detail="You must upload at least 2 images and at most 6 images.")

        # Tạo thư mục lưu ảnh nếu chưa có
        save_dir = os.path.join(os.getcwd(), "Images")
        os.makedirs(save_dir, exist_ok=True)

        uploaded_images = []

        # Lưu từng ảnh vào thư mục và DB
        for file in files:
            # Đường dẫn lưu file
            save_path = os.path.join(save_dir, file.filename)

            # Lưu file vào ổ đĩa
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_url = f"static/images/profile/{file.filename}"
            # Tạo entity ProfileImage
            image_data = ProfileImage(
                title=file.filename,
                url=image_url,
                alt=os.path.splitext(file.filename)[0],
                upload_date=datetime.utcnow(),
                profile_id=profile_id  # Liên kết với profile_id
            )

            # Lưu vào DB
            db.add(image_data)
            db.commit()
            db.refresh(image_data)

            uploaded_images.append(image_data)

        # Lấy Profile và gắn những ảnh đã upload vào images của Profile
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if profile:
            profile.images.extend(uploaded_images)  # Thêm ảnh vào danh sách images của profile
            db.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Profile with ID {profile_id} not found in the database")

        return uploaded_images
    
    def save_profile_image(db: Session, profile_id: int, filename: str):
        file_url = f"static/images/profile/{filename}"
        
        image = ProfileImage(
            profile_id=profile_id, 
            url=file_url,
            title=filename,
            alt=None,
            upload_date=datetime.utcnow())
        db.add(image)
        db.commit()
        db.refresh(image)
        return image
    
    @staticmethod
    def get_profile_images_by_id(id: int, db: Session) -> FileResponse:
        image = db.query(ProfileImage).filter(ProfileImage.id == id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image_path = os.path.join(os.getcwd(), image.url)
        if not os.path.isfile(image_path):
           image_path += ".jpg"
           image_path += ".jpeg"
           image_path += ".png"

        if not os.path.isfile(image_path):
            raise HTTPException(status_code=404, detail="File not found on server")

        mime_type, _ = mimetypes.guess_type(image_path)
        return FileResponse(path=image_path, media_type=mime_type or "application/octet-stream")

    @staticmethod
    def delete_profile_image(image_id: int, db: Session):
        image = db.query(ProfileImage).filter(ProfileImage.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        # Xóa file ảnh khỏi ổ đĩa nếu tồn tại
        file_path = os.path.join(os.getcwd(), image.url)
        if os.path.isfile(file_path):
            os.remove(file_path)

        # Xóa bản ghi khỏi DB
        db.delete(image)
        db.commit()
        return {"detail": "Deleted successfully"}
    
    
    
    
    