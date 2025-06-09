import os
import uuid
import requests
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import logging
import io
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StableDiffusionService:
    """Service for generating images using Stable Diffusion"""
    
    def __init__(self):
        self.output_dir = Path("generated_images")
        self.output_dir.mkdir(exist_ok=True)
        self.hf_api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        # note to self get a free token at https://huggingface.co/settings/tokens
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN", "")
        
    def _generate_with_huggingface(self, prompt: str) -> Image.Image:
        """Generate image using Hugging Face API"""
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "guidance_scale": 7.5,
                "num_inference_steps": 25,
                "width": 512,
                "height": 512
            }
        }
        
        try:
            response = requests.post(self.hf_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                return image
            elif response.status_code == 503:
                logger.warning("Model loading, trying alternative API...")
                return self._generate_with_alternative_api(prompt)
            else:
                logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                raise Exception(f"API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"HuggingFace API failed: {e}")
            raise
    
    def _generate_with_alternative_api(self, prompt: str) -> Image.Image:
        """Alternative free AI image generation API"""
        try:
            api_url = "https://image.pollinations.ai/prompt/"
            encoded_prompt = prompt.replace(" ", "%20").replace(",", "%2C")
            full_url = f"{api_url}{encoded_prompt}?width=512&height=512&nologo=true"
            
            logger.info(f"Requesting image from: {full_url}")
            response = requests.get(full_url, timeout=10)
            
            logger.info(f"Response status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'unknown')}, Size: {len(response.content)} bytes")
            
            if response.status_code == 200:
                if len(response.content) < 1000:
                    logger.error(f"Response too small ({len(response.content)} bytes), likely not an image")
                    raise Exception("Response too small to be a valid image")
                
                try:
                    image = Image.open(io.BytesIO(response.content))
                    logger.info(f"Successfully loaded image: {image.size}, format: {image.format}")
                    return image
                except Exception as img_error:
                    logger.error(f"Failed to load image from response: {img_error}")
                    raise Exception(f"Invalid image data: {img_error}")
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text[:200]}")
                raise Exception(f"Alternative API failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Alternative API failed: {e}")
            raise
        
    def _generate_placeholder_image(self, prompt: str, width: int = 512, height: int = 512) -> Image.Image:
        """Generate a placeholder image with the prompt text"""
        img = Image.new('RGB', (width, height), color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            r = int(70 + (180 - 70) * y / height)
            g = int(130 + (100 - 130) * y / height) 
            b = int(180 + (200 - 180) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        try:
            font_paths = [
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/Arial.ttf",
                "/Library/Fonts/Arial.ttf"
            ]
            font = None
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, 28)
                    break
                except:
                    continue
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        text = f"🎨 Dream: {prompt}"
        if len(text) > 60:
            text = f"🎨 Dream: {prompt[:55]}..."
    
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x+2, y+2), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        draw.rectangle([40, 40, width-40, height-40], outline=(255, 255, 255), width=3)
        draw.rectangle([50, 50, width-50, height-50], outline=(255, 255, 255, 128), width=1)
        
        for i in range(10):
            star_x = 60 + (i * 40) % (width - 120)
            star_y = 60 + (i * 37) % (height - 120)
            draw.ellipse([star_x-2, star_y-2, star_x+2, star_y+2], fill=(255, 255, 255))
        
        return img
    
    def generate_image(self, prompt: str, filename: Optional[str] = None) -> dict:
        """
        Generate an image from a text prompt using real AI
        
        Args:
            prompt: Text description of the image to generate
            filename: Optional custom filename (without extension)
            
        Returns:
            dict: Contains both file_path and image_url
        """
        try:
            if filename is None:
                filename = f"dream_{uuid.uuid4().hex[:8]}"
            
            logger.info(f"🎨 Generating REAL AI image for prompt: {prompt[:50]}...")
            
            try:
                if self.hf_token:
                    logger.info("Using Hugging Face Stable Diffusion API...")
                    image = self._generate_with_huggingface(prompt)
                    logger.info("✅ Successfully generated AI image with Hugging Face!")
                else:
                    logger.info("Using free Pollinations.AI for real AI generation...")
                    image = self._generate_with_alternative_api(prompt)
                    logger.info("✅ Successfully generated AI image with Pollinations.AI!")
                    
            except Exception as ai_error:
                logger.error(f"❌ AI generation failed with error: {ai_error}")
                logger.error(f"❌ Error type: {type(ai_error).__name__}")
                logger.error(f"❌ Full traceback:", exc_info=True)
                logger.info("🔄 Falling back to enhanced placeholder...")
                image = self._generate_placeholder_image(prompt)
            
            image_path = self.output_dir / f"{filename}.png"
            image.save(image_path, quality=95)
            
            image_url = f"/static/generated_images/{filename}.png"
            
            logger.info(f"Image saved to: {image_path}")
            logger.info(f"Accessible URL: {image_url}")
            
            return {
                "file_path": str(image_path),
                "image_url": image_url
            }
            
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            raise

stable_diffusion_service = StableDiffusionService()

def generate_image(prompt: str, filename: Optional[str] = None) -> dict:
    """
    Convenience function to generate an image
    
    Args:
        prompt: Text description of the image to generate
        filename: Optional custom filename (without extension)
        
    Returns:
        dict: Contains both file_path and image_url
    """
    return stable_diffusion_service.generate_image(prompt, filename)

if __name__ == "__main__":
    pass 