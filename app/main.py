# app/main.py
from fastapi import FastAPI
from app.routers import ProfileController, ImageController

app = FastAPI()
app.include_router(ProfileController.router)
app.include_router(ImageController.router)

@app.get("/")
def root():
    return {"message": "Dating app API is live"}