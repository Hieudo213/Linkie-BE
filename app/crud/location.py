from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime

async def upsert_user_location(db: AsyncSession, user_id: int, lat: float, lng: float):
    db.execute(text("""
        INSERT INTO user_locations (user_id, location, last_updated)
        VALUES (:user_id, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326), :now)
        ON CONFLICT (user_id) DO UPDATE SET
        location = EXCLUDED.location,
        last_updated = EXCLUDED.last_updated
    """), {"user_id": user_id, "lat": lat, "lng": lng, "now": datetime.utcnow()})
    db.commit()

async def get_nearby_user_profiles(db: AsyncSession, user_ids: list[int]):
    if not user_ids:
        return []
    placeholders = ", ".join(f":uid{i}" for i in range(len(user_ids)))
    params = {f"uid{i}": uid for i, uid in enumerate(user_ids)}

    query = text(f"""
        SELECT u.id, u.username, u.phone_number, u.email
        FROM users u
        WHERE u.id IN ({placeholders})
        ORDER BY u.id
    """)
    # Đúng cú pháp: `await db.execute(...)`
    result = db.execute(query, params)

    # Lấy kết quả từ CursorResult
    rows = result.fetchall()  # ✅ KHÔNG được `await` dòng này nữa

    # Trả về danh sách dict cho dễ xử lý
    columns = result.keys()
    return [dict(zip(columns, row)) for row in rows]
