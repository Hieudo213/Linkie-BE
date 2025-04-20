# app/crud/user.py
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ProfileModel import Profile
from app.schemas.ProfileDTO import ProfileCreate


def get_all_profiles(db: Session):
    return db.query(Profile).all()

def create_profile(db: Session, profile_in: ProfileCreate) -> Profile:
    new_profile = Profile(
        full_name=profile_in.full_name,
        gender=profile_in.gender,
        date_of_birth=profile_in.date_of_birth,
        bio=profile_in.bio,
        created_at=datetime.utcnow(),
        target_type=profile_in.target_type,
        hobby=profile_in.hobby
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def update_profile(db: Session, profile_id: int, update_data: ProfileCreate) -> Profile:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, profile_id: int) -> str:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return f"Xoá thành công profile có id: {profile_id}"

def get_profile_by_id(db: Session, profile_id: int) -> Profile:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile