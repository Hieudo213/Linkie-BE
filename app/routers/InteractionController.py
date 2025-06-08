from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.InteractionService import InteractionService

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/like/{liked_id}/{liker_id}")
def like_user(
    liked_id: int,
    liker_id: int,
    db: Session = Depends(get_db),
):
    result = InteractionService.like_user(db, liker_id, liked_id)
    return result