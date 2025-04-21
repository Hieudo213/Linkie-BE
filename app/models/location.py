from sqlalchemy import Column, DateTime, Integer
from geoalchemy2 import Geography
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserLocation(Base):
    __tablename__ = "user_locations"

    user_id = Column(Integer, primary_key=True)
    location = Column(Geography(geometry_type="POINT", srid=4326))
    last_updated = Column(DateTime, default=datetime.utcnow)
