#!/usr/bin/env python3
"""
Direct test of user registration functionality
"""

from app.db.session import SessionLocal, engine, Base
from app.db.models import User
from app.db.schemas.user import UserCreate
from app.api.v1.routes.auth import register_user

def test_registration_direct():
    """Test user registration directly"""
    
    Base.metadata.create_all(bind=engine)
    
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    
    db = SessionLocal()
    
    try:
        result = register_user(user_data, db)
        print(f"✅ Registration successful!")
        print(f"User ID: {result.id}")
        print(f"Email: {result.email}")
        print(f"Created at: {result.created_at}")
        
        user_in_db = db.query(User).filter(User.email == "test@example.com").first()
        if user_in_db:
            print("✅ User found in database!")
        else:
            print("❌ User not found in database!")
            
        return True
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_registration_direct() 