from fastapi import UploadFile, File, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.ImageService import ImageService

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image = ImageService.upload_image(file, db)
    return JSONResponse(content={
        "message": "Image uploaded successfully",
        "image": {
            "id": image.id,
            "title": image.title,
            "url": image.url,
            "alt": image.alt,
            "upload_date": image.upload_date.isoformat()
        }
    })

@router.get("/{id}")
def serve_image(id: int, db: Session = Depends(get_db)):
    return ImageService.get_image_by_id(id, db)

@router.delete("/delete/{id}")
def delete_image(id: int, db: Session = Depends(get_db)):
    ImageService.delete_image_by_id(id, db)
    return {"message": f"Image with ID {id} deleted successfully (file + database)"}
