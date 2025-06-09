from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ....db.session import get_db
from ....db.models.video import Video
from ....db.schemas.video import VideoRequest, VideoResponse, VideoCreate
from ....services.video_generation import generate_video
from ....core.security import get_current_user_optional

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=VideoResponse)
async def create_video(
    video_request: VideoRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """
    Create a new video from a text prompt
    """
    try:
        logger.info(f"Generating video for prompt: {video_request.prompt}")
        
        result = generate_video(video_request.prompt)
        
        video_data = VideoCreate(
            prompt=video_request.prompt,
            video_path=result["file_path"],
            video_url=result["video_url"],
            user_id=current_user.id if current_user else None
        )
        
        db_video = Video(**video_data.model_dump())
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        
        return VideoResponse.model_validate(db_video)
        
    except Exception as e:
        logger.error(f"Video generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@router.get("/me", response_model=List[VideoResponse])
async def get_user_videos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """
    Get the current user's video history
    Requires authentication
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    videos = db.query(Video).filter(Video.user_id == current_user.id).order_by(Video.created_at.desc()).all()
    return [VideoResponse.model_validate(video) for video in videos]

@router.get("/", response_model=List[VideoResponse])
async def get_recent_videos(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get recent public videos (for gallery/showcase)
    """
    videos = db.query(Video).order_by(Video.created_at.desc()).limit(limit).all()
    return [VideoResponse.model_validate(video) for video in videos] 