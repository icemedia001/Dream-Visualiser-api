from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import api_router
from .db.session import engine, Base
from .db.models import user, dream, video
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mind's Eye Dream-Visualizer",
    description="An AI-powered dream visualizer app",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("generated_images", exist_ok=True)
os.makedirs("generated_videos", exist_ok=True)

app.mount("/static/generated_images", StaticFiles(directory="generated_images"), name="generated_images")
app.mount("/static/generated_videos", StaticFiles(directory="generated_videos"), name="generated_videos")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "OK"} 