from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.InteractionModel import Like, Match


class InteractionService:
    @staticmethod
    def like_user(db: Session, liker_id: int, liked_id: int) -> dict:
        if liker_id == liked_id:
            raise HTTPException(status_code=400, detail="Cannot like yourself.")

        # Check đã like trước đó chưa
        existing = db.query(Like).filter_by(liker_id=liker_id, liked_id=liked_id).first()
        if existing:
            return {"message": "Already liked this user."}

        # Lưu tương tác
        new_like = Like(liker_id=liker_id, liked_id=liked_id, timestamp=datetime.utcnow())
        db.add(new_like)
        db.commit()

        # Kiểm tra nếu người kia cũng đã like lại
        reciprocal = db.query(Like).filter_by(liker_id=liked_id, liked_id=liker_id).first()
        if reciprocal:
            new_match = Match(user1_id=min(liker_id, liked_id), user2_id=max(liker_id, liked_id))
            db.add(new_match)
            db.commit()
            return {"message": "It’s a match!", "match": True}

        return {"message": "Like recorded.", "match": False}
