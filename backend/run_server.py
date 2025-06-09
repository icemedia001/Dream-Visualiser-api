#!/usr/bin/env python3
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting Dream Visualizer API server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔗 API docs will be at: http://localhost:8000/docs")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc() 