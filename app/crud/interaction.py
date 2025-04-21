from sqlalchemy.orm import Session
# from app.models.interaction import Interaction, Conversation
from app.models.interaction import Interaction
from app.models.conversation import Conversation

from sqlalchemy.exc import IntegrityError

def create_interaction(db: Session, user_id: int, profile_id: int, is_like: bool):
    """
    Ghi nhận hành động swipe (like/dislike) của người dùng
    """
    # Kiểm tra xem người dùng đã swipe người này chưa
    interaction = Interaction(userId=user_id, profileId=profile_id, isLike=is_like)

    db.add(interaction)
    db.commit()

    # Kiểm tra nếu cả 2 người đã like nhau thì tạo conversation
    if is_like:
        match = db.query(Interaction).filter(
            Interaction.userId == profile_id,
            Interaction.profileId == user_id,
            Interaction.isLike == True
        ).first()

        if match:
            # Tạo conversation nếu cả 2 đều like nhau
            create_conversation(db, user_id, profile_id)

    return interaction

def create_conversation(db: Session, user1_id: int, user2_id: int):
    """
    Tạo một cuộc trò chuyện giữa 2 người dùng
    """
    conversation = Conversation(user1=user1_id, user2=user2_id)

    db.add(conversation)
    db.commit()
    return conversation
