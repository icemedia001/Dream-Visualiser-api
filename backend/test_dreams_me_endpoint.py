#!/usr/bin/env python3
"""
Test the GET /api/v1/dreams/me endpoint specifically
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

def test_dreams_me_endpoint():
    """Test the dreams/me endpoint step by step"""
    
    print("🧪 Testing GET /api/v1/dreams/me endpoint")
    
    print("📊 Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    client = TestClient(app)
    
    print("\n🚫 Test 1: Unauthenticated request")
    response = client.get("/api/v1/dreams/me")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.status_code != 500 else 'Server error'}")
    assert response.status_code == 403
    print("✅ Unauthenticated request correctly rejected")
    
    print("\n👤 Test 2: Creating test user")
    db = SessionLocal()
    try:
        test_user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpass123")
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ Created user with ID: {test_user.id}")
    finally:
        db.close()
    
    print("\n🔑 Test 3: Creating JWT token")
    token = create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ JWT token created")
    
    print("\n📚 Test 4: Authenticated request (no dreams)")
    response = client.get("/api/v1/dreams/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        dreams = response.json()
        print(f"   Dreams found: {len(dreams)}")
        assert len(dreams) == 0
        print("✅ Empty dreams list returned correctly")
    else:
        print(f"   Error: {response.json()}")
        return False
    
    print("\n🎨 Test 5: Creating dream for user")
    dream_data = {"prompt": "A beautiful sunset over mountains"}
    response = client.post("/api/v1/dreams/", json=dream_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        dream_response = response.json()
        print(f"   Dream created with ID: {dream_response['id']}")
        print("✅ Dream created successfully")
    else:
        print(f"   Error: {response.json()}")
        return False
    
    print("\n📚 Test 6: Authenticated request (with dreams)")
    response = client.get("/api/v1/dreams/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        dreams = response.json()
        print(f"   Dreams found: {len(dreams)}")
        assert len(dreams) == 1
        
        dream = dreams[0]
        print(f"   Dream prompt: {dream['prompt']}")
        print(f"   Dream user_id: {dream['user_id']}")
        print(f"   Dream image_url: {dream['image_url']}")
        
        assert dream['user_id'] == test_user.id
        assert dream['prompt'] == "A beautiful sunset over mountains"
        assert dream['image_url'].startswith("/static/generated_images/")
        
        print("✅ User's dream returned correctly")
    else:
        print(f"   Error: {response.json()}")
        return False
    
    print("\n🎉 All tests passed! GET /api/v1/dreams/me is working correctly.")
    return True

if __name__ == "__main__":
    try:
        success = test_dreams_me_endpoint()
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed!")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc() 