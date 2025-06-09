from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class DreamBase(BaseModel):
    prompt: str = Field(..., min_length=1, description="Dream description prompt")
    
    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()

class DreamCreate(DreamBase):
    pass

class Dream(DreamBase):
    id: int
    user_id: Optional[int] = None
    image_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DreamResponse(DreamBase):
    id: int
    user_id: Optional[int] = None
    image_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True 