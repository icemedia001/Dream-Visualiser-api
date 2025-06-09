#!/usr/bin/env python3
"""
Test video generation functionality
"""

from app.services.video_generation import generate_video
import os
import requests

def test_video_generation():
    """Test video generation service"""
    
    try:
        print("🎬 Testing video generation service...")
        
        prompt = "A serene lake at sunset"
        result = generate_video(prompt, "test_video")
        
        video_path = result["file_path"]
        video_url = result["video_url"]
        
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            print(f"✅ Video generated successfully!")
            print(f"   Path: {video_path}")
            print(f"   URL: {video_url}")
            print(f"   Size: {file_size} bytes")
        else:
            print(f"❌ Video file not found: {video_path}")
            return False
        
        print(f"\n🎉 Video generation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Video generation test failed: {e}")
        return False

def test_video_api():
    """Test video API endpoint"""
    
    try:
        print("\n🌐 Testing video API endpoint...")
        
        api_url = "http://localhost:8000/api/v1/videos/"
        payload = {"prompt": "A magical forest with glowing mushrooms"}
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API test passed!")
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ API test failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    service_success = test_video_generation()
    
    api_success = test_video_api()
    
    if service_success and api_success:
        print(f"\n🎉 All video tests passed!")
    else:
        print(f"\n❌ Some tests failed.") 