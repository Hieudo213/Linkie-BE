from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.core.connection_manager import manager
import asyncio

def create_notification(db: Session, user_id: int, title: str, content: str, image: str = None, link: str = None):
    noti = Notification(user_id=user_id, title=title, content=content, image=image, link=link)
    db.add(noti)
    db.commit()
    db.refresh(noti)

    asyncio.create_task(manager.send_notification(user_id, {
        # "id": noti.id,
        "title": noti.title,
        "content": noti.content,
        "image": noti.image,
        "link": noti.link,
        "created_at": str(noti.created_at),
        "updated_at": str(noti.updated_at) if noti.updated_at else None
    }))

    return noti

def get_notifications(db: Session, user_id: int, index: int = 0, count: int = 20):
    return db.query(Notification).filter(Notification.user_id == user_id)\
        .order_by(Notification.created_at.desc()).offset(index).limit(count).all()

def delete_notification(db: Session, user_id: int, noti_id: int):
    noti = db.query(Notification).filter(Notification.id == noti_id, Notification.user_id == user_id).first()
    if noti:
        db.delete(noti)
        db.commit()
    return noti
