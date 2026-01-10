"""
Image generation module using Google Gemini AI
"""

import google.generativeai as genai
from PIL import Image
import io
import time
from typing import Optional
from .config import config


class ImageGenerator:
    """Generate images for e-book using Google Gemini"""
    
    def __init__(self):
        """Initialize the image generator with Gemini API"""
        genai.configure(api_key=config.gemini_api_key)
        # Note: As of now, Gemini's image generation might be limited
        # We'll use the Imagen model if available, otherwise create placeholder images
        try:
            self.model = genai.GenerativeModel('gemini-pro-vision')
        except (AttributeError, ValueError) as e:
            self.model = None
    
    def generate_image(self, prompt: str, width: int = 512, height: int = 512) -> Optional[Image.Image]:
        """
        Generate an image based on the prompt
        
        Args:
            prompt: Description of the image to generate
            width: Width of the image
            height: Height of the image
            
        Returns:
            PIL Image object or None if generation fails
        """
        # Note: Google Gemini currently doesn't have direct image generation
        # We'll create a placeholder with the prompt text
        # In production, you would use Imagen API or another image generation service
        
        try:
            # Create a placeholder image with gradient background
            img = Image.new('RGB', (width, height), color=(240, 240, 250))
            
            # Add some visual interest
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Draw a gradient-like effect
            for i in range(height):
                color_value = int(240 - (i / height) * 50)
                draw.rectangle([(0, i), (width, i+1)], fill=(color_value, color_value, color_value + 10))
            
            # Add text showing it's an AI-generated placeholder
            try:
                # Try to use a basic font
                font = ImageFont.load_default()
            except (OSError, IOError, ImportError):
                font = None
            
            # Draw prompt text (truncated if too long)
            text = f"Ilustração:\n{prompt[:100]}"
            if font:
                # Calculate text position
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                # Draw text with shadow for better visibility
                draw.text((x+2, y+2), text, fill=(100, 100, 100), font=font)
                draw.text((x, y), text, fill=(50, 50, 100), font=font)
            
            return img
            
        except Exception as e:
            print(f"Erro ao gerar imagem: {e}")
            # Return a simple colored placeholder
            return Image.new('RGB', (width, height), color=(200, 220, 240))
    
    def generate_cover_image(self, title: str, theme: str, width: int = 800, height: int = 1200) -> Image.Image:
        """
        Generate a cover image for the e-book
        
        Args:
            title: Title of the e-book
            theme: Theme of the e-book
            width: Width of the cover
            height: Height of the cover
            
        Returns:
            PIL Image object
        """
        # Create an attractive cover image
        img = Image.new('RGB', (width, height), color=(30, 60, 100))
        
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Draw a gradient background
        for i in range(height):
            r = int(30 + (i / height) * 100)
            g = int(60 + (i / height) * 80)
            b = int(100 + (i / height) * 120)
            draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
        
        # Draw decorative elements
        for i in range(5):
            x = int(width * 0.1 + i * width * 0.15)
            y = int(height * 0.2)
            size = 50
            draw.ellipse([(x, y), (x + size, y + size)], fill=(255, 255, 255, 50))
        
        try:
            # Use default font
            title_font = ImageFont.load_default()
            theme_font = ImageFont.load_default()
        except (OSError, IOError, ImportError):
            title_font = None
            theme_font = None
        
        # Draw title
        if title_font:
            # Word wrap title
            words = title.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=title_font)
                if bbox[2] - bbox[0] < width - 100:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw title lines
            y_offset = height // 3
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                # Draw shadow
                draw.text((x+3, y_offset+3), line, fill=(0, 0, 0), font=title_font)
                # Draw text
                draw.text((x, y_offset), line, fill=(255, 255, 255), font=title_font)
                y_offset += bbox[3] - bbox[1] + 20
            
            # Draw theme
            theme_text = f"Sobre: {theme}"
            bbox = draw.textbbox((0, 0), theme_text, font=theme_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height - 150
            
            draw.text((x+2, y+2), theme_text, fill=(0, 0, 0), font=theme_font)
            draw.text((x, y), theme_text, fill=(200, 200, 200), font=theme_font)
        
        return img
