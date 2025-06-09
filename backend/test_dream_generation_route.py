#!/usr/bin/env python3
"""
Test dream generation API route
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, engine
from app.db.session import Base
from app.db.models.dream import Dream
from app.db.models.user import User
import requests

def test_dream_generation_route():
    """Test the dream generation route"""
    
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    client = TestClient(app)
    
    dream_data = {
        "prompt": "A magical forest with glowing mushrooms and fairy lights"
    }
    
    print(f"Testing dream generation with prompt: {dream_data['prompt']}")
    
    response = client.post("/api/v1/dreams/", json=dream_data)
    
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")
    
    assert response.status_code == 200
    
    dream_response = response.json()
    
    assert "id" in dream_response
    assert "user_id" in dream_response
    assert "prompt" in dream_response
    assert "image_url" in dream_response
    assert "created_at" in dream_response
    
    print(f"✅ Dream created successfully!")
    print(f"   - Dream ID: {dream_response['id']}")
    print(f"   - User ID: {dream_response['user_id']}")
    print(f"   - Prompt: {dream_response['prompt']}")
    print(f"   - Image URL: {dream_response['image_url']}")
    print(f"   - Created at: {dream_response['created_at']}")
    
    image_url = dream_response['image_url']
    filename = image_url.split('/')[-1]
    image_file_path = f"generated_images/{filename}"
    
    if os.path.exists(image_file_path):
        file_size = os.path.getsize(image_file_path)
        print(f"✅ Image file exists: {image_file_path} ({file_size} bytes)")
    else:
        print(f"❌ Image file not found: {image_file_path}")
    
    db = SessionLocal()
    try:
        db_dream = db.query(Dream).filter(Dream.id == dream_response['id']).first()
        if db_dream:
            print(f"✅ Dream found in database with ID: {db_dream.id}")
        else:
            print(f"❌ Dream not found in database")
    finally:
        db.close()

if __name__ == "__main__":
    test_dream_generation_route() 