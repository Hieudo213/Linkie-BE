# app/main.py
from fastapi import FastAPI
from app.routers import ProfileController
from app.core.database import engine, Base
from app.routers import ProfileController
app = FastAPI()
app.include_router(ProfileController.router)

@app.get("/")
def root():
    return {"message": "Dating app API is live"}