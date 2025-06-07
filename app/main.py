# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routers import ProfileController, ImageController, AuthController, AccountController, LocationController

app = FastAPI()
app.include_router(AuthController.router)
app.include_router(AccountController.router)
app.include_router(ProfileController.router)
app.include_router(ImageController.router)
app.include_router(LocationController.router)
@app.get("/")
def root():
    return {"message": "Dating app API is live"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Linkie API",
        version="1.0.0",
        description="Linkie API with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi