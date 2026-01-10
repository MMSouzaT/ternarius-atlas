"""
Main E-book Generator class that orchestrates the entire generation process
"""

import os
from typing import List, Optional
from PIL import Image

from .config import config, Config
from .text_generator import TextGenerator
from .image_generator import ImageGenerator
from .page_composer import PageComposer


class EbookGenerator:
    """
    Main class to generate complete e-books from a theme
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the e-book generator
        
        Args:
            output_dir: Directory where e-book pages will be saved
        """
        self.output_dir = output_dir
        self.config = config
        self.text_generator = TextGenerator()
        self.image_generator = ImageGenerator()
        self.page_composer = PageComposer(self.config)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_ebook(
        self,
        theme: str,
        num_chapters: int = 3,
        pages_per_chapter: int = 2,
        include_images: bool = True,
        author: str = "Gerado por IA com Ternarius Atlas"
    ) -> List[str]:
        """
        Generate a complete e-book from a theme
        
        Args:
            theme: The main theme/topic for the e-book
            num_chapters: Number of chapters to generate
            pages_per_chapter: Number of pages per chapter
            include_images: Whether to include AI-generated images
            author: Author name to display
            
        Returns:
            List of file paths to generated page images
        """
        print(f"🚀 Iniciando geração do e-book sobre: {theme}")
        print(f"📚 Configuração: {num_chapters} capítulos, {pages_per_chapter} páginas por capítulo")
        print("-" * 60)
        
        generated_pages = []
        
        # Step 1: Generate e-book structure
        print("\n📝 Etapa 1: Gerando estrutura do e-book...")
        structure = self.text_generator.generate_ebook_structure(theme, num_chapters)
        ebook_title = structure['title']
        chapters = structure['chapters']
        
        print(f"✅ Título: {ebook_title}")
        for i, chapter_title in enumerate(chapters, 1):
            print(f"   Capítulo {i}: {chapter_title}")
        
        # Step 2: Generate cover page
        print("\n🎨 Etapa 2: Gerando capa do e-book...")
        cover_image = self.image_generator.generate_cover_image(
            ebook_title, 
            theme,
            self.config.DEFAULT_PAGE_WIDTH,
            self.config.DEFAULT_PAGE_HEIGHT
        )
        
        cover_path = os.path.join(self.output_dir, "page_000_cover.png")
        cover_image.save(cover_path)
        generated_pages.append(cover_path)
        print(f"✅ Capa salva: {cover_path}")
        
        # Step 3: Generate title page
        print("\n📄 Etapa 3: Gerando página de título...")
        title_page = self.page_composer.create_title_page(ebook_title, author)
        title_path = os.path.join(self.output_dir, "page_001_title.png")
        title_page.save(title_path)
        generated_pages.append(title_path)
        print(f"✅ Página de título salva: {title_path}")
        
        # Step 4: Generate chapters
        page_counter = 2
        
        for chapter_idx, chapter_title in enumerate(chapters, 1):
            print(f"\n📖 Etapa 4.{chapter_idx}: Gerando capítulo {chapter_idx}: {chapter_title}")
            
            # Generate chapter content
            print(f"   ⏳ Gerando conteúdo do capítulo...")
            chapter_pages = self.text_generator.generate_chapter_content(
                theme, 
                chapter_title, 
                pages_per_chapter
            )
            
            # Generate pages for this chapter
            for page_idx, page_content in enumerate(chapter_pages, 1):
                print(f"   📄 Processando página {page_idx}/{len(chapter_pages)}...")
                
                # Optionally generate an image for the page
                page_image = None
                if include_images and page_idx == 1:  # Add image to first page of each chapter
                    print(f"      🎨 Gerando imagem ilustrativa...")
                    image_prompt = self.text_generator.generate_image_prompt(
                        theme, 
                        chapter_title, 
                        page_content
                    )
                    page_image = self.image_generator.generate_image(image_prompt, 400, 300)
                
                # Compose the page
                page = self.page_composer.create_page(
                    text=page_content,
                    image=page_image,
                    page_number=page_counter,
                    title=chapter_title if page_idx == 1 else ""
                )
                
                # Save the page
                page_filename = f"page_{page_counter:03d}_ch{chapter_idx}_p{page_idx}.png"
                page_path = os.path.join(self.output_dir, page_filename)
                page.save(page_path)
                generated_pages.append(page_path)
                print(f"   ✅ Página salva: {page_filename}")
                
                page_counter += 1
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🎉 E-book gerado com sucesso!")
        print(f"📚 Total de páginas: {len(generated_pages)}")
        print(f"📁 Diretório de saída: {self.output_dir}")
        print("=" * 60)
        
        return generated_pages
    
    def generate_quick_ebook(self, theme: str) -> List[str]:
        """
        Generate a quick/demo e-book with minimal configuration
        
        Args:
            theme: The theme for the e-book
            
        Returns:
            List of file paths to generated page images
        """
        return self.generate_ebook(
            theme=theme,
            num_chapters=2,
            pages_per_chapter=2,
            include_images=True
        )
