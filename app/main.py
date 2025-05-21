# app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import profile, location, interaction, interaction_list, conversation, chat, notification, package

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dating App API",
    description="API cho dự án Dating App",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Dating app API is live"}

app.include_router(profile.router)
app.include_router(location.router)
app.include_router(interaction.router)
app.include_router(interaction_list.router)
app.include_router(conversation.router)
app.include_router(chat.router)
app.include_router(notification.router)
app.include_router(package.router)

