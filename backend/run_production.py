#!/usr/bin/env python3
"""
Production server runner for Dream Visualizer API

This script provides a production-ready server configuration with:
- Proper logging
- Security settings
- Error handling
- Health checks
"""

import uvicorn
import logging
import os
from app.main import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Start the production server"""
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    
    logger.info("🚀 Starting Dream Visualizer API (Production)")
    logger.info(f"📍 Server: {host}:{port}")
    logger.info(f"👥 Workers: {workers}")
    logger.info(f"🔗 API docs: http://{host}:{port}/docs")
    
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            workers=workers,
            log_level="info",
            access_log=True,
            reload=False,  # Disable reload in production
            loop="uvloop" if os.name != "nt" else "asyncio",  # Use uvloop on Unix systems
        )
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        raise

if __name__ == "__main__":
    main() 