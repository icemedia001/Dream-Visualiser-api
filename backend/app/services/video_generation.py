#!/usr/bin/env python3
"""
Video generation service using free APIs
"""

import os
import uuid
import requests
import logging
from pathlib import Path
from typing import Optional
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoGenerationService:
    """Service for generating videos from text prompts using free APIs"""
    
    def __init__(self):
        self.output_dir = Path("generated_videos")
        self.output_dir.mkdir(exist_ok=True)
        
        self.free_apis = [
            {
                "name": "Pika Labs (if available)",
                "url": "https://api.pika.art/generate",  # TODO: add this
                "enabled": False
            }
        ]
    
    def _generate_with_free_api(self, prompt: str) -> str:
        """
        Try to generate video using free APIs
        Note: Most free video APIs are limited or require tokens
        """
        # TODO: Implement actual free API calls when available
        raise Exception("No free video APIs currently available")
    
    def _generate_placeholder_video(self, prompt: str, duration: int = 3, fps: int = 24) -> str:
        """
        Generate a placeholder video with animated text and simple graphics
        
        Args:
            prompt: Text prompt to display in video
            duration: Duration in seconds
            fps: Frames per second
            
        Returns:
            str: Path to generated video file
        """
        width, height = 512, 512
        total_frames = duration * fps
        
        temp_filename = f"temp_{uuid.uuid4().hex[:8]}.mp4"
        temp_path = self.output_dir / temp_filename
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(temp_path), fourcc, fps, (width, height))
        
        try:
            for frame_num in range(total_frames):
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                
                progress = frame_num / total_frames
                for y in range(height):
                    color_intensity = int(50 + 100 * np.sin(progress * 2 * np.pi + y / height * np.pi))
                    color_intensity = max(0, min(255, color_intensity))
                    frame[y, :] = [color_intensity, max(0, color_intensity // 2), max(0, color_intensity // 3)]
                
                pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_frame)
                
                time_offset = progress * 2 * np.pi
                
                center_x, center_y = width // 2, height // 2
                radius = 50 + 20 * np.sin(time_offset * 3)
                circle_color = (255, 255, 255, 128)
                draw.ellipse([center_x - radius, center_y - radius, 
                            center_x + radius, center_y + radius], 
                           outline=circle_color, width=2)
                
                words = prompt.split()
                lines = []
                current_line = ""
                max_width = width - 60
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if len(test_line) * 8 < max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                line_height = 25
                total_text_height = len(lines) * line_height
                start_y = center_y - total_text_height // 2
                
                for i, line in enumerate(lines):
                    y_pos = start_y + i * line_height
                    draw.text((32, y_pos + 2), line, fill=(0, 0, 0))
                    alpha = int(255 * (0.7 + 0.3 * np.sin(time_offset + i * 0.5)))
                    text_color = (255, 255, 255)
                    draw.text((30, y_pos), line, fill=text_color)
                
                title = "AI Video Generation"
                draw.text((width // 2 - 80, 30), title, fill=(255, 255, 255))
                
                frame_text = f"Frame {frame_num + 1}/{total_frames}"
                draw.text((width - 150, height - 20), frame_text, fill=(200, 200, 200))
                
                cv2_frame = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
                video_writer.write(cv2_frame)
            
            video_writer.release()
            return str(temp_path)
            
        except Exception as e:
            video_writer.release()
            if temp_path.exists():
                temp_path.unlink()
            raise e
    
    def generate_video(self, prompt: str, filename: Optional[str] = None) -> dict:
        """
        Generate a video from a text prompt
        
        Args:
            prompt: Text description for the video
            filename: Optional custom filename (without extension)
            
        Returns:
            dict: Contains file_path and video_url
        """
        try:
            if filename is None:
                filename = f"video_{uuid.uuid4().hex[:8]}"
            
            logger.info(f"🎬 Generating video for prompt: {prompt[:50]}...")
            
            try:
                logger.info("Attempting to use free video generation APIs...")
                video_path = self._generate_with_free_api(prompt)
                logger.info("✅ Successfully generated video with free API!")
                
            except Exception as api_error:
                logger.warning(f"Free API failed: {api_error}")
                logger.info("🔄 Falling back to placeholder video...")
                video_path = self._generate_placeholder_video(prompt)
                logger.info("✅ Generated placeholder video!")
            
            final_path = self.output_dir / f"{filename}.mp4"
            if video_path != str(final_path):
                Path(video_path).rename(final_path)
            
            video_url = f"/static/generated_videos/{filename}.mp4"
            
            logger.info(f"Video saved to: {final_path}")
            logger.info(f"Accessible URL: {video_url}")
            
            return {
                "file_path": str(final_path),
                "video_url": video_url
            }
            
        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            raise

video_generation_service = VideoGenerationService()

def generate_video(prompt: str, filename: Optional[str] = None) -> dict:
    """
    Convenience function to generate a video
    
    Args:
        prompt: Text description for the video
        filename: Optional custom filename (without extension)
        
    Returns:
        dict: Contains file_path and video_url
    """
    return video_generation_service.generate_video(prompt, filename)

if __name__ == "__main__":
    result = generate_video("A peaceful sunset over the ocean with gentle waves")
    print(f"Generated video: {result}") 