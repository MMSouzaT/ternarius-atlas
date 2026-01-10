"""
Configuration module for Ternarius Atlas
Handles API keys and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the e-book generator"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY não encontrada. "
                "Por favor, crie um arquivo .env baseado no .env.example "
                "e adicione sua chave da API do Google Gemini."
            )
    
    # Default settings for e-book generation
    DEFAULT_PAGE_WIDTH = 800
    DEFAULT_PAGE_HEIGHT = 1200
    DEFAULT_FONT_SIZE = 24
    DEFAULT_TITLE_FONT_SIZE = 36
    DEFAULT_TEXT_COLOR = (0, 0, 0)  # Black
    DEFAULT_BACKGROUND_COLOR = (255, 255, 255)  # White
    DEFAULT_PADDING = 50
    DEFAULT_LINE_SPACING = 1.5
    
    # AI generation settings
    MAX_TOKENS_PER_PAGE = 500
    TEMPERATURE = 0.7
    IMAGE_SIZE = "512x512"


# Global config instance
config = Config()
