# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.profile import Base, Profile  # Import Base và Profile từ profile.py

# DATABASE_URL = "postgresql://tinder_user:quangteo@localhost:5432/tinder_db"

# DATABASE_URL = "postgresql://postgres:linkiesteam05@db.lfyxsnujmwljbncwiout.supabase.co:5432/postgres"

DATABASE_URL = "postgresql://postgres.lfyxsnujmwljbncwiout:linkiesteam05@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo bảng
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()