from fastapi import APIRouter
from .routes import auth, dreams, videos

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dreams.router, prefix="/dreams", tags=["dreams"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
