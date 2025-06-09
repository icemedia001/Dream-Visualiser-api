#!/usr/bin/env python3
"""
Test image generation functionality
"""

from app.services.stable_diffusion import generate_image
import os

def test_image_generation():
    """Test image generation service"""
    
    try:
        test_prompts = [
            "A serene mountain landscape at sunset",
            "A futuristic city with flying cars",
            "A peaceful garden with blooming flowers"
        ]
        
        print("🎨 Testing image generation service...")
        
        for i, prompt in enumerate(test_prompts):
            print(f"\n📝 Generating image {i+1}: {prompt}")
            
            result = generate_image(prompt, f"test_image_{i+1}")
            
            image_path = result["file_path"]
            image_url = result["image_url"]
            
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"✅ Image generated successfully!")
                print(f"   Path: {image_path}")
                print(f"   URL: {image_url}")
                print(f"   Size: {file_size} bytes")
            else:
                print(f"❌ Image file not found: {image_path}")
                return False
        
        print(f"\n🎉 All tests passed! Image generation service is working.")
        return True
        
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

if __name__ == "__main__":
    test_image_generation() 