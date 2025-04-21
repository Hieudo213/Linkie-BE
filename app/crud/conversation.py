from sqlalchemy.orm import Session
# from app.models.interaction import Conversation
# from app.models.interaction import Interaction
from app.models.conversation import Conversation


def get_conversations(db: Session, user_id: int):
    """
    Lấy tất cả các cuộc trò chuyện của người dùng
    """
    conversations = db.query(Conversation).filter(
        (Conversation.user1 == user_id) | (Conversation.user2 == user_id)
    ).all()

    return conversations
