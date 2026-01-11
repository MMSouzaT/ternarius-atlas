"""
Page composer module to combine text and images into e-book pages
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
from .config import Config


class PageComposer:
    """Compose e-book pages by combining text and images"""
    
    def __init__(self, config: Config = None):
        """
        Initialize the page composer
        
        Args:
            config: Configuration object (uses default if not provided)
        """
        self.config = config or Config()
    
    def create_page(
        self,
        text: str,
        image: Optional[Image.Image] = None,
        page_number: int = 1,
        title: str = "",
        width: int = None,
        height: int = None
    ) -> Image.Image:
        """
        Create a single e-book page with text and optional image
        
        Args:
            text: Text content for the page
            image: Optional image to include on the page
            page_number: Page number to display
            title: Optional title for the page
            width: Page width (uses default if not provided)
            height: Page height (uses default if not provided)
            
        Returns:
            PIL Image object representing the page
        """
        width = width or self.config.DEFAULT_PAGE_WIDTH
        height = height or self.config.DEFAULT_PAGE_HEIGHT
        padding = self.config.DEFAULT_PADDING
        
        # Create blank page
        page = Image.new('RGB', (width, height), self.config.DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(page)
        
        try:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
        except (OSError, IOError, ImportError):
            font = None
            title_font = None
        
        current_y = padding
        
        # Draw title if provided
        if title and title_font:
            title_lines = self._wrap_text(title, width - 2 * padding, draw, title_font)
            for line in title_lines:
                draw.text((padding, current_y), line, fill=self.config.DEFAULT_TEXT_COLOR, font=title_font)
                bbox = draw.textbbox((0, 0), line, font=title_font)
                current_y += (bbox[3] - bbox[1]) + 10
            
            current_y += 20  # Extra space after title
        
        # Draw image if provided
        if image:
            # Resize image to fit page with some margin
            image_max_width = width - 2 * padding
            image_max_height = (height - current_y - padding - 100)  # Leave space for text
            
            image_resized = self._resize_image_to_fit(image, image_max_width, image_max_height)
            
            # Center image horizontally
            image_x = (width - image_resized.width) // 2
            page.paste(image_resized, (image_x, current_y))
            current_y += image_resized.height + 20
        
        # Draw text content
        if text and font:
            # Wrap text to fit page width
            text_lines = self._wrap_text(text, width - 2 * padding, draw, font)
            
            line_height = self._get_line_height(draw, font)
            
            for line in text_lines:
                # Check if we have space for this line
                if current_y + line_height > height - padding - 30:  # Leave space for page number
                    break
                
                draw.text((padding, current_y), line, fill=self.config.DEFAULT_TEXT_COLOR, font=font)
                current_y += line_height
        
        # Draw page number at the bottom
        if font:
            page_num_text = f"— {page_number} —"
            bbox = draw.textbbox((0, 0), page_num_text, font=font)
            text_width = bbox[2] - bbox[0]
            page_num_x = (width - text_width) // 2
            page_num_y = height - padding
            draw.text((page_num_x, page_num_y), page_num_text, fill=(150, 150, 150), font=font)
        
        # Draw border
        draw.rectangle([(5, 5), (width-5, height-5)], outline=(200, 200, 200), width=2)
        
        return page
    
    def create_title_page(
        self,
        title: str,
        author: str = "Gerado por IA",
        width: int = None,
        height: int = None
    ) -> Image.Image:
        """
        Create a title page for the e-book
        
        Args:
            title: Title of the e-book
            author: Author name
            width: Page width
            height: Page height
            
        Returns:
            PIL Image object representing the title page
        """
        width = width or self.config.DEFAULT_PAGE_WIDTH
        height = height or self.config.DEFAULT_PAGE_HEIGHT
        
        page = Image.new('RGB', (width, height), self.config.DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(page)
        
        try:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
        except (OSError, IOError, ImportError):
            title_font = None
            author_font = None
        
        # Draw decorative elements
        for i in range(3):
            y = int(height * 0.2 + i * 30)
            draw.line([(width * 0.3, y), (width * 0.7, y)], fill=(150, 150, 200), width=2)
        
        # Draw title in the center
        if title_font:
            title_lines = self._wrap_text(title, width - 100, draw, title_font)
            total_height = len(title_lines) * (self._get_line_height(draw, title_font))
            start_y = (height - total_height) // 2
            
            for line in title_lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, start_y), line, fill=self.config.DEFAULT_TEXT_COLOR, font=title_font)
                start_y += self._get_line_height(draw, title_font)
        
        # Draw author at the bottom
        if author_font:
            bbox = draw.textbbox((0, 0), author, font=author_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height - 100
            draw.text((x, y), author, fill=(100, 100, 100), font=author_font)
        
        # Draw border
        draw.rectangle([(10, 10), (width-10, height-10)], outline=(100, 100, 150), width=3)
        
        return page
    
    def _wrap_text(self, text: str, max_width: int, draw: ImageDraw, font) -> list:
        """
        Wrap text to fit within max_width
        
        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            draw: ImageDraw object
            font: Font to use
            
        Returns:
            List of text lines
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _get_line_height(self, draw: ImageDraw, font) -> int:
        """
        Get the height of a line of text
        
        Args:
            draw: ImageDraw object
            font: Font to use
            
        Returns:
            Line height in pixels
        """
        bbox = draw.textbbox((0, 0), "Ay", font=font)
        return int((bbox[3] - bbox[1]) * self.config.DEFAULT_LINE_SPACING)
    
    def _resize_image_to_fit(self, image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        """
        Resize image to fit within max dimensions while maintaining aspect ratio
        
        Args:
            image: Image to resize
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Resized image
        """
        ratio = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        
        # Use LANCZOS resampling for best quality (compatible with older Pillow versions)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS
        
        return image.resize((new_width, new_height), resample)
    
    def add_text_to_cover(self, background_image: Image.Image, title: str) -> Image.Image:
        """
        Add title text to a cover image
        
        Args:
            background_image: Base image for the cover
            title: Book title to add
            
        Returns:
            Image with text overlay
        """
        # Create a copy to avoid modifying original
        result = background_image.copy()
        draw = ImageDraw.Draw(result)
        
        width, height = result.size
        
        try:
            # Try to use a larger font for title
            title_font = ImageFont.load_default()
        except:
            title_font = None
        
        # Add semi-transparent overlay for text readability
        overlay = Image.new('RGBA', result.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Draw semi-transparent rectangle
        padding = 50
        rect_y = int(height * 0.3)
        rect_height = int(height * 0.4)
        overlay_draw.rectangle(
            [(padding, rect_y), (width - padding, rect_y + rect_height)],
            fill=(255, 255, 255, 200)
        )
        
        # Composite overlay
        result = Image.alpha_composite(result.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(result)
        
        # Draw title text
        title_lines = self._wrap_text(title, width - 2 * padding - 20, draw, title_font)
        
        # Calculate total text height
        line_height = self._get_line_height(draw, title_font)
        total_text_height = len(title_lines) * line_height
        
        # Center text vertically in the overlay
        start_y = rect_y + (rect_height - total_text_height) // 2
        
        for i, line in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            text_y = start_y + i * line_height
            
            # Draw text with shadow for better readability
            shadow_offset = 2
            draw.text((text_x + shadow_offset, text_y + shadow_offset), line, fill=(100, 100, 100), font=title_font)
            draw.text((text_x, text_y), line, fill=(20, 20, 20), font=title_font)
        
        return result
    
    def add_text_to_page(self, background_image: Image.Image, text: str, page_number: int = 1) -> Image.Image:
        """
        Add text content to a page image with good readability
        
        Args:
            background_image: Base image
            text: Text content to add
            page_number: Page number
            
        Returns:
            Image with text overlay
        """
        # Create a copy
        result = background_image.copy()
        width, height = result.size
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Create semi-transparent text area at bottom
        overlay = Image.new('RGBA', result.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Calculate text area size
        padding = 30
        text_area_height = int(height * 0.35)  # Use bottom 35% for text
        text_area_y = height - text_area_height
        
        # Draw semi-transparent background for text
        overlay_draw.rectangle(
            [(0, text_area_y), (width, height)],
            fill=(255, 255, 255, 220)
        )
        
        # Composite overlay
        result = Image.alpha_composite(result.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(result)
        
        # Wrap and draw text
        text_lines = self._wrap_text(text, width - 2 * padding, draw, font)
        line_height = self._get_line_height(draw, font)
        
        current_y = text_area_y + padding
        
        # Limit number of lines to fit in text area
        max_lines = (text_area_height - 2 * padding - 30) // line_height  # Leave space for page number
        
        for i, line in enumerate(text_lines):
            if i >= max_lines:
                # Add ellipsis if text is too long
                if i == max_lines:
                    draw.text((padding, current_y), "...", fill=(50, 50, 50), font=font)
                break
            
            draw.text((padding, current_y), line, fill=(30, 30, 30), font=font)
            current_y += line_height
        
        # Add page number
        page_num_text = f"— {page_number} —"
        bbox = draw.textbbox((0, 0), page_num_text, font=font)
        text_width = bbox[2] - bbox[0]
        page_num_x = (width - text_width) // 2
        page_num_y = height - padding + 5
        draw.text((page_num_x, page_num_y), page_num_text, fill=(100, 100, 100), font=font)
        
        return result
