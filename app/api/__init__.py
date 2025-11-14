from app.api.routes.auth import auth_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)