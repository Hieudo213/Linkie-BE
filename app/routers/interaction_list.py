from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core.database import get_db
from app.schemas.interaction_list import InteractionListResponse
from app.crud.interaction_list import get_user_interactions
from typing import List

router = APIRouter()

@router.get("/interactions", response_model=InteractionListResponse)
async def get_interactions(userId: int, isLike: bool, db: Session = Depends(get_db)):
    """
    API lấy danh sách đã like
    """
    # Truy vấn cơ sở dữ liệu để lấy danh sách interactions
    interactions = get_user_interactions(db, userId, isLike)
    
    if not interactions:
        raise HTTPException(status_code=404, detail="No interactions found")

    return {"code": "200", "message": "Success", "profiles": interactions}
