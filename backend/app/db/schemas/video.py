from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class VideoRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Video description prompt")
    
    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()

class VideoResponse(BaseModel):
    id: int
    prompt: str
    video_url: str
    user_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class VideoCreate(BaseModel):
    prompt: str
    video_path: str
    video_url: str
    user_id: Optional[int] = None 