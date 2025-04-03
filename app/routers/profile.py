# app/routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.profile import ProfileOut
from app.crud.profile import get_all_profiles
from app.core.database import get_db

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/", response_model=List[ProfileOut])
def read_profiles(db: Session = Depends(get_db)):
    return get_all_profiles(db)