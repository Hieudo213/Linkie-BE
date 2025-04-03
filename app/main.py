# app/main.py
from fastapi import FastAPI
from app.routers import profile
from app.core.database import engine, Base
from app.routers import profile
app = FastAPI()
app.include_router(profile.router)

@app.get("/")
def root():
    return {"message": "Dating app API is live"}