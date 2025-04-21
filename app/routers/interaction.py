from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.interaction import create_interaction
from app.schemas.interaction import InteractionOut
from app.core.database import get_db

router = APIRouter()

@router.post("/interactions", response_model=InteractionOut)
def create_like_or_dislike(
    user_id: int, profile_id: int, is_like: bool, db: Session = Depends(get_db)
):
    """
    API ghi nhận hành động swipe (like/dislike) và kiểm tra match
    """
    interaction = create_interaction(db, user_id, profile_id, is_like)
    return interaction
