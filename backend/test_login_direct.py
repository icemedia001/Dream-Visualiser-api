#!/usr/bin/env python3
"""
Direct test of user login functionality
"""

from app.db.session import SessionLocal, engine, Base
from app.db.models import User
from app.db.schemas.user import UserCreate, UserLogin
from app.api.v1.routes.auth import register_user, login_user

def test_login_direct():
    """Test user login directly"""
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        user_data = UserCreate(
            email="login_test@example.com",
            password="testpassword123"
        )
        
        try:
            registered_user = register_user(user_data, db)
            print(f"✅ User registered: {registered_user.email}")
        except Exception as e:
            print(f"⚠️  User might already exist: {e}")
        
        login_data = UserLogin(
            email="login_test@example.com",
            password="testpassword123"
        )
        
        token_response = login_user(login_data, db)
        print(f"✅ Login successful!")
        print(f"Access Token: {token_response['access_token'][:50]}...")
        print(f"Token Type: {token_response['token_type']}")
        
        try:
            wrong_login = UserLogin(
                email="login_test@example.com",
                password="wrongpassword"
            )
            login_user(wrong_login, db)
            print("❌ Wrong password should have failed!")
        except Exception as e:
            print(f"✅ Wrong password correctly rejected: {type(e).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_login_direct() 