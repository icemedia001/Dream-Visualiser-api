#!/usr/bin/env python3
"""
Test static image serving for generated dream images
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

def test_static_image_serving():
    """Test that generated images are accessible via static URLs"""
    
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    client = TestClient(app)
    
    dream_data = {
        "prompt": "A serene mountain landscape with clouds"
    }
    
    print(f"🎨 Creating dream with prompt: {dream_data['prompt']}")
    
    response = client.post("/api/v1/dreams/", json=dream_data)
    
    print(f"Response status: {response.status_code}")
    assert response.status_code == 200
    
    dream_response = response.json()
    image_url = dream_response['image_url']
    
    print(f"📸 Generated image URL: {image_url}")
    
    print(f"🌐 Testing static image access...")
    image_response = client.get(image_url)
    
    print(f"Image response status: {image_response.status_code}")
    print(f"Image response headers: {dict(image_response.headers)}")
    
    assert image_response.status_code == 200
    
    content_type = image_response.headers.get("content-type")
    assert "image" in content_type.lower(), f"Expected image content type, got: {content_type}"
    
    image_data = image_response.content
    assert len(image_data) > 0, "Image data is empty"
    
    png_signature = b'\x89PNG\r\n\x1a\n'
    assert image_data.startswith(png_signature), "Response is not a valid PNG file"
    
    print(f"✅ Static image serving test passed!")
    print(f"   - Image URL: {image_url}")
    print(f"   - Content-Type: {content_type}")
    print(f"   - Image size: {len(image_data)} bytes")
    print(f"   - Valid PNG signature: ✅")
    
    print(f"🚫 Testing access to non-existent image...")
    not_found_response = client.get("/static/generated_images/nonexistent.png")
    print(f"Non-existent image response status: {not_found_response.status_code}")
    assert not_found_response.status_code == 404
    print(f"✅ Non-existent image correctly returns 404")

if __name__ == "__main__":
    test_static_image_serving() 