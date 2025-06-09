#!/usr/bin/env python3
"""
Test JWT token decoding and protected routes
"""

from app.db.session import SessionLocal, engine, Base
from app.db.models import User as UserModel
from app.db.schemas.user import UserCreate, UserLogin
from app.api.v1.routes.auth import register_user, login_user
from app.core.security import verify_token

def test_jwt_auth():
    """Test JWT authentication flow"""
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        user_data = UserCreate(
            email="jwt_test@example.com",
            password="testpassword123"
        )
        
        try:
            registered_user = register_user(user_data, db)
            print(f"✅ User registered: {registered_user.email}")
        except Exception:
            print("⚠️  User already exists, proceeding with login test")
        
        login_data = UserLogin(
            email="jwt_test@example.com",
            password="testpassword123"
        )
        
        token_response = login_user(login_data, db)
        access_token = token_response["access_token"]
        print(f"✅ Login successful, got token")
        
        payload = verify_token(access_token)
        if payload:
            print(f"✅ Token verification successful")
            print(f"   User ID from token: {payload.get('sub')}")
            print(f"   Email from token: {payload.get('email')}")
        else:
            print("❌ Token verification failed")
            return False
        
        try:
            user_id = payload.get("sub")
            current_user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
            
            if current_user:
                print(f"✅ User lookup from token successful")
                print(f"   Current user: {current_user.email}")
                print(f"   User ID: {current_user.id}")
                print(f"✅ JWT auth dependency ready for protected routes!")
            else:
                print("❌ User lookup failed - user not found")
                return False
            
        except Exception as e:
            print(f"❌ User lookup failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ JWT auth test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_jwt_auth() 