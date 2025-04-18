# app/routers/user.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.ProfileService import get_all_profiles, create_profile, update_profile, delete_profile, get_profile_by_id
from app.schemas.ProfileDTO import ProfileCreate
from app.schemas.ProfileDTO import ProfileOut

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/", response_model=List[ProfileOut])
def read_profiles(db: Session = Depends(get_db)):
    return get_all_profiles(db)

@router.post("/create", response_model=ProfileOut)
def add_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return create_profile(db=db, profile_in=profile)

@router.put("/update/{profile_id}", response_model=ProfileOut)
def update_existing_profile(profile_id: int, update_data: ProfileCreate, db: Session = Depends(get_db)):
    return update_profile(db=db, profile_id=profile_id, update_data=update_data)

@router.delete("/delete/{profile_id}", response_model=str)
def remove_profile(profile_id: int, db: Session = Depends(get_db)):
    return delete_profile(db=db, profile_id=profile_id)

@router.get("/{profile_id}", response_model=ProfileOut)
def read_profile_by_id(profile_id: int, db: Session = Depends(get_db)):
    return get_profile_by_id(db=db, profile_id=profile_id)
