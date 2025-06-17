from geoalchemy2.functions import ST_SetSRID, ST_MakePoint, ST_Distance
from sqlalchemy.orm import Session
from app.models.UserModel import Account
from app.models.LocationModel import Location
from datetime import datetime
from geopy.geocoders import Nominatim

class LocationService:

    @staticmethod
    def update_location(account_id: int, latitude: float, longitude: float, db: Session):
        # Truy vấn account từ database
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return None  # Không tìm thấy tài khoản

        # Tạo điểm địa lý từ latitude và longitude
        point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)

        # Kiểm tra xem tài khoản đã có location chưa
        location = db.query(Location).filter(Location.account_id == account_id).first()

        if location:
            # Cập nhật vị trí nếu đã có location
            location.latitude = latitude
            location.longitude = longitude
            location.point = point  # Cập nhật trường point
            location.last_updated = datetime.utcnow()  # Cập nhật thời gian thay đổi vị trí
            db.commit()
            db.refresh(location)
        else:
            # Tạo mới location nếu chưa có
            location = Location(
                latitude=latitude,
                longitude=longitude,
                point=point,
                account_id=account_id,
                last_updated=datetime.utcnow()
            )
            db.add(location)
            db.commit()
            db.refresh(location)

        return location

    @staticmethod
    def find_nearby_users(current_lat: float, current_lon: float, db: Session, radius: int = 10):
        # Tạo điểm của người dùng hiện tại
        current_location = ST_SetSRID(ST_MakePoint(current_lon, current_lat), 4326)

        # Truy vấn những người dùng có vị trí trong bán kính radius km
        nearby_users = db.query(Account).join(Location).filter(
            ST_Distance(Location.point, current_location) <= radius * 1000  # Chuyển km thành m
        ).all()

        return nearby_users

    @staticmethod
    def get_location_name(latitude, longitude):
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), language='vi')

        if location:
            return location.address  # Trả về tên địa điểm (thành phố, quốc gia...)
        else:
            return "Location not found"

