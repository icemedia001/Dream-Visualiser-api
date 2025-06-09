from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.dream import Dream
from app.db.schemas.dream import DreamCreate, DreamResponse
from app.services.stable_diffusion import generate_image
from app.core.security import get_current_user_optional, get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=DreamResponse)
async def create_dream(
    dream_data: DreamCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Create a new dream by generating an image from the prompt.
    Supports both authenticated and anonymous users.
    """
    try:
        logger.info(f"Creating dream with prompt: {dream_data.prompt}")
        
        result = generate_image(dream_data.prompt)
        image_path = result["file_path"]
        image_url = result["image_url"]
        
        logger.info(f"Image generated and saved to: {image_path}")
        
        db_dream = Dream(
            user_id=current_user.id if current_user else None,
            prompt=dream_data.prompt,
            image_path=image_path
        )
        
        db.add(db_dream)
        db.commit()
        db.refresh(db_dream)
        
        logger.info(f"Dream created with ID: {db_dream.id}")
        
        response = DreamResponse(
            id=db_dream.id,
            user_id=db_dream.user_id,
            prompt=db_dream.prompt,
            image_url=image_url,
            created_at=db_dream.created_at
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to create dream: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate dream image")

@router.get("/me", response_model=List[DreamResponse])
async def get_my_dreams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all dreams for the current authenticated user.
    Requires authentication.
    """
    logger.info(f"Fetching dreams for user ID: {current_user.id}")
    
    dreams = db.query(Dream).filter(Dream.user_id == current_user.id).all()
    
    logger.info(f"Found {len(dreams)} dreams for user {current_user.id}")
    
    response_dreams = []
    for dream in dreams:
        filename = dream.image_path.split('/')[-1]
        image_url = f"/static/generated_images/{filename}"
        
        response_dreams.append(DreamResponse(
            id=dream.id,
            user_id=dream.user_id,
            prompt=dream.prompt,
            image_url=image_url,
            created_at=dream.created_at
        ))
    
    return response_dreams 