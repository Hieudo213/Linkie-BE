from sqlalchemy.orm import Session
from app.models.notification import Notification


def get_notifications(db: Session, user_id: int, index: int = 0, count: int = 10):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .offset(index)
        .limit(count)
        .all()
    )


def delete_notification(db: Session, user_id: int, notification_id: int):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if notification:
        db.delete(notification)
        db.commit()
    return notification
