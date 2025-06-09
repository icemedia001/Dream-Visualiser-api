#!/usr/bin/env python3
"""
Test script to verify database connection and create SQLite file
"""

from app.db.session import engine, Base, SessionLocal
from app.db.models.user import User
from app.db.models.dream import Dream

def test_db_connection():
    """Test database connection and create tables"""
    try:
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        result = db.execute("SELECT 1")
        print(f"Database connection successful! Test query result: {result.scalar()}")
        
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [table[0] for table in tables]
        print(f"Created tables: {table_names}")
        
        db.close()
        print("SQLite database file created successfully!")
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db_connection() 