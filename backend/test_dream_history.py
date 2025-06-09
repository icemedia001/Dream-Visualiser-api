#!/usr/bin/env python3
"""
Test dream history functionality for authenticated users
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
from app.core.security import create_access_token, get_password_hash
import requests

def test_dream_history():
    """Test authenticated user dream history functionality"""
    
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    client = TestClient(app)
    
    db = SessionLocal()
    try:
        test_user = User(
            email="testuser@example.com",
            hashed_password=get_password_hash("testpassword123")
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        test_user2 = User(
            email="testuser2@example.com", 
            hashed_password=get_password_hash("testpassword456")
        )
        db.add(test_user2)
        db.commit()
        db.refresh(test_user2)
        
        print(f"✅ Created test users with IDs: {test_user.id}, {test_user2.id}")
        
    finally:
        db.close()
    
    user1_token = create_access_token(data={"sub": str(test_user.id)})
    user2_token = create_access_token(data={"sub": str(test_user2.id)})
    
    headers_user1 = {"Authorization": f"Bearer {user1_token}"}
    headers_user2 = {"Authorization": f"Bearer {user2_token}"}
    
    print(f"✅ Generated JWT tokens for both users")
    
    print("\n🎨 Creating dreams for User 1...")
    user1_dreams = [
        {"prompt": "A mystical forest with ancient trees"},
        {"prompt": "A cyberpunk cityscape at night"},
        {"prompt": "A peaceful mountain lake at sunrise"}
    ]
    
    user1_dream_responses = []
    for dream_data in user1_dreams:
        response = client.post("/api/v1/dreams/", json=dream_data, headers=headers_user1)
        assert response.status_code == 200
        user1_dream_responses.append(response.json())
        print(f"   Created dream: {dream_data['prompt'][:30]}...")
    
    print("\n🎨 Creating dreams for User 2...")
    user2_dreams = [
        {"prompt": "A dragon soaring through clouds"},
        {"prompt": "An underwater coral reef city"}
    ]
    
    user2_dream_responses = []
    for dream_data in user2_dreams:
        response = client.post("/api/v1/dreams/", json=dream_data, headers=headers_user2)
        assert response.status_code == 200
        user2_dream_responses.append(response.json())
        print(f"   Created dream: {dream_data['prompt'][:30]}...")
    
    print("\n🎨 Creating anonymous dream...")
    anonymous_dream = {"prompt": "An anonymous dream about space"}
    response = client.post("/api/v1/dreams/", json=anonymous_dream)
    assert response.status_code == 200
    anonymous_response = response.json()
    print(f"   Created anonymous dream: {anonymous_dream['prompt']}")
    
    print("\n📚 Getting User 1's dream history...")
    response = client.get("/api/v1/dreams/me", headers=headers_user1)
    assert response.status_code == 200
    
    user1_history = response.json()
    print(f"   User 1 has {len(user1_history)} dreams")
    
    assert len(user1_history) == 3, f"Expected 3 dreams for user 1, got {len(user1_history)}"
    
    for i, dream in enumerate(user1_history):
        assert dream["user_id"] == test_user.id
        assert dream["prompt"] == user1_dreams[i]["prompt"]
        assert "image_url" in dream
        assert dream["image_url"].startswith("/static/generated_images/")
        print(f"   ✅ Dream {i+1}: {dream['prompt'][:30]}...")
    
    print("\n📚 Getting User 2's dream history...")
    response = client.get("/api/v1/dreams/me", headers=headers_user2)
    assert response.status_code == 200
    
    user2_history = response.json()
    print(f"   User 2 has {len(user2_history)} dreams")
    
    assert len(user2_history) == 2, f"Expected 2 dreams for user 2, got {len(user2_history)}"
    
    for i, dream in enumerate(user2_history):
        assert dream["user_id"] == test_user2.id
        assert dream["prompt"] == user2_dreams[i]["prompt"]
        assert "image_url" in dream
        assert dream["image_url"].startswith("/static/generated_images/")
        print(f"   ✅ Dream {i+1}: {dream['prompt'][:30]}...")
    
    print("\n🚫 Testing unauthenticated access...")
    response = client.get("/api/v1/dreams/me")
    assert response.status_code == 403
    print(f"   ✅ Unauthenticated request correctly returned 403")
    
    print("\n🚫 Testing invalid token...")
    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/api/v1/dreams/me", headers=invalid_headers)
    assert response.status_code == 401
    print(f"   ✅ Invalid token correctly returned 401")
    
    print("\n🖼️  Testing image URL accessibility...")
    test_dream = user1_history[0]
    image_response = client.get(test_dream["image_url"])
    assert image_response.status_code == 200
    assert "image" in image_response.headers.get("content-type", "").lower()
    print(f"   ✅ Image URL accessible: {test_dream['image_url']}")
    
    print(f"\n✅ All dream history tests passed!")
    print(f"   - User 1: {len(user1_history)} dreams")
    print(f"   - User 2: {len(user2_history)} dreams") 
    print(f"   - Anonymous dreams correctly excluded from user histories")
    print(f"   - Authentication properly enforced")
    print(f"   - Image URLs are accessible")

if __name__ == "__main__":
    test_dream_history()