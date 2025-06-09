#!/usr/bin/env python3
"""
Integration test for dream generation functionality
Uses pytest + httpx for comprehensive testing
"""

import pytest
import sys
import os
import asyncio
import uuid
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, engine, Base
from app.db.models.dream import Dream
from app.db.models.user import User
from app.core.security import create_access_token, get_password_hash

TEST_DATABASE_URL = "sqlite:///./test_dreams_integration.db"

@pytest.fixture(scope="session")
def setup_test_database():
    """Set up test database before all tests"""
    print("\n🔧 Setting up test database...")
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    yield
    
    print("\n🧹 Cleaning up test database...")
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Create a test user in the database"""
    db = SessionLocal()
    try:
        unique_email = f"integration_test_{uuid.uuid4().hex[:8]}@example.com"
        user = User(
            email=unique_email,
            hashed_password=get_password_hash("integration_test_password")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for test user"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

class TestDreamGenerationIntegration:
    """Integration tests for dream generation functionality"""
    
    def test_anonymous_dream_generation(self, client, setup_test_database):
        """Test dream generation for anonymous users"""
        print("\n🎭 Testing anonymous dream generation...")
        
        dream_data = {
            "prompt": "A serene mountain landscape with snow-capped peaks"
        }
        
        response = client.post("/api/v1/dreams/", json=dream_data)
        
        assert response.status_code == 200
        dream = response.json()
        
        assert "id" in dream
        assert "user_id" in dream
        assert "prompt" in dream
        assert "image_url" in dream
        assert "created_at" in dream
        
        assert dream["user_id"] is None
        assert dream["prompt"] == dream_data["prompt"]
        assert dream["image_url"].startswith("/static/generated_images/")
        
        image_filename = dream["image_url"].split("/")[-1]
        image_path = Path(f"generated_images/{image_filename}")
        assert image_path.exists(), f"Generated image not found: {image_path}"
        assert image_path.stat().st_size > 0, "Generated image file is empty"
        
        print(f"✅ Anonymous dream created successfully: {dream['id']}")
    
    def test_authenticated_dream_generation(self, client, setup_test_database, test_user, auth_headers):
        """Test dream generation for authenticated users"""
        print(f"\n👤 Testing authenticated dream generation for user {test_user.id}...")
        
        dream_data = {
            "prompt": "A magical underwater city with glowing coral structures"
        }
        
        response = client.post("/api/v1/dreams/", json=dream_data, headers=auth_headers)
        
        assert response.status_code == 200
        dream = response.json()
        
        assert dream["user_id"] == test_user.id
        assert dream["prompt"] == dream_data["prompt"]
        assert dream["image_url"].startswith("/static/generated_images/")
        
        image_filename = dream["image_url"].split("/")[-1]
        image_path = Path(f"generated_images/{image_filename}")
        assert image_path.exists(), f"Generated image not found: {image_path}"
        assert image_path.stat().st_size > 0, "Generated image file is empty"
        
        print(f"✅ Authenticated dream created successfully: {dream['id']}")
    
    def test_database_persistence(self, client, setup_test_database, test_user, auth_headers):
        """Test that dreams are properly stored in database"""
        print("\n💾 Testing database persistence...")
        
        dream_data = {"prompt": "A futuristic cityscape with flying vehicles"}
        response = client.post("/api/v1/dreams/", json=dream_data, headers=auth_headers)
        assert response.status_code == 200
        dream_response = response.json()
        
        db = SessionLocal()
        try:
            stored_dream = db.query(Dream).filter(Dream.id == dream_response["id"]).first()
            assert stored_dream is not None, "Dream not found in database"
            assert stored_dream.user_id == test_user.id
            assert stored_dream.prompt == dream_data["prompt"]
            assert stored_dream.image_path is not None
            assert stored_dream.created_at is not None
            
            print(f"✅ Dream properly stored in database: ID {stored_dream.id}")
        finally:
            db.close()
    
    def test_image_url_accessibility(self, client, setup_test_database):
        """Test that generated image URLs are accessible via static route"""
        print("\n🖼️  Testing image URL accessibility...")
        
        dream_data = {"prompt": "A peaceful zen garden with bamboo"}
        response = client.post("/api/v1/dreams/", json=dream_data)
        assert response.status_code == 200
        dream = response.json()
        
        image_response = client.get(dream["image_url"])
        assert image_response.status_code == 200
        
        content_type = image_response.headers.get("content-type", "")
        assert "image" in content_type.lower(), f"Expected image content type, got: {content_type}"
        
        content_length = len(image_response.content)
        assert content_length > 0, "Image response is empty"
        
        print(f"✅ Image URL accessible: {dream['image_url']} ({content_length} bytes)")
    
    def test_multiple_dreams_same_user(self, client, setup_test_database, test_user, auth_headers):
        """Test creating multiple dreams for the same user"""
        print(f"\n🎨 Testing multiple dreams for user {test_user.id}...")
        
        prompts = [
            "A tropical beach at sunset",
            "A mysterious dark forest with glowing fireflies", 
            "A steampunk airship floating through clouds"
        ]
        
        created_dreams = []
        for i, prompt in enumerate(prompts):
            dream_data = {"prompt": prompt}
            response = client.post("/api/v1/dreams/", json=dream_data, headers=auth_headers)
            assert response.status_code == 200
            
            dream = response.json()
            assert dream["user_id"] == test_user.id
            assert dream["prompt"] == prompt
            created_dreams.append(dream)
            
            print(f"   Dream {i+1}: {prompt[:30]}... (ID: {dream['id']})")
        
        history_response = client.get("/api/v1/dreams/me", headers=auth_headers)
        assert history_response.status_code == 200
        
        user_dreams = history_response.json()
        assert len(user_dreams) >= len(prompts), "Not all dreams found in user history"
        
        print(f"✅ Created {len(created_dreams)} dreams successfully")
    
    def test_invalid_prompt_handling(self, client, setup_test_database):
        """Test handling of invalid prompts"""
        print("\n❌ Testing invalid prompt handling...")
        
        response = client.post("/api/v1/dreams/", json={"prompt": ""})
        if response.status_code == 200:
            print("   Empty prompt accepted (current behavior)")
        else:
            print(f"   Empty prompt rejected with status: {response.status_code}")
        
        response = client.post("/api/v1/dreams/", json={})
        assert response.status_code == 422, "Missing prompt should return validation error"
        print("   Missing prompt correctly rejected with 422")
        
        long_prompt = "A" * 10000
        response = client.post("/api/v1/dreams/", json={"prompt": long_prompt})
        print(f"   Long prompt response: {response.status_code}")
        
        print("✅ Invalid prompt handling tested")
    
    def test_concurrent_dream_generation(self, client, setup_test_database):
        """Test handling multiple concurrent dream requests"""
        print("\n⚡ Testing concurrent dream generation...")
        
        # Note/TODO: Use asyncio or threading later
        prompts = [
            "A red rose in morning dew",
            "A blue butterfly on a flower", 
            "A green meadow with wildflowers"
        ]
        
        responses = []
        for prompt in prompts:
            dream_data = {"prompt": prompt}
            response = client.post("/api/v1/dreams/", json=dream_data)
            responses.append((prompt, response))
        
        for prompt, response in responses:
            assert response.status_code == 200, f"Failed for prompt: {prompt}"
            dream = response.json()
            assert dream["prompt"] == prompt
            
        print(f"✅ Successfully handled {len(responses)} concurrent requests")

def test_full_integration_workflow(client, setup_test_database, test_user, auth_headers):
    """Test complete workflow: anonymous -> register -> authenticate -> create dreams -> view history"""
    print("\n🔄 Testing full integration workflow...")
    
    anonymous_dream_data = {"prompt": "An anonymous dream about space exploration"}
    response = client.post("/api/v1/dreams/", json=anonymous_dream_data)
    assert response.status_code == 200
    anonymous_dream = response.json()
    assert anonymous_dream["user_id"] is None
    print("   ✅ Step 1: Anonymous dream created")
    
    auth_dream_data = {"prompt": "An authenticated dream about time travel"}
    response = client.post("/api/v1/dreams/", json=auth_dream_data, headers=auth_headers)
    assert response.status_code == 200
    auth_dream = response.json()
    assert auth_dream["user_id"] == test_user.id
    print("   ✅ Step 2: Authenticated dream created")
    
    response = client.get("/api/v1/dreams/me", headers=auth_headers)
    assert response.status_code == 200
    user_dreams = response.json()
    
    user_dream_ids = [dream["id"] for dream in user_dreams]
    assert anonymous_dream["id"] not in user_dream_ids
    assert auth_dream["id"] in user_dream_ids
    print("   ✅ Step 3: User history correctly filtered")
    
    for dream in [anonymous_dream, auth_dream]:
        image_response = client.get(dream["image_url"])
        assert image_response.status_code == 200
        assert len(image_response.content) > 0
    print("   ✅ Step 4: All images accessible")
    
    print("🎉 Full integration workflow completed successfully!")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"]) 