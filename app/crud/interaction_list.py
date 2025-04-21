from sqlalchemy.orm import Session
# from app.models import Interaction
from app.models.interaction import Interaction

def get_user_interactions(db: Session, user_id: int, is_like: bool):
    # Lọc các interaction theo user_id và trạng thái like/dislike
    return db.query(Interaction).filter(Interaction.userId == user_id, Interaction.isLike == is_like).all()
