"""
Text generation module using Google Gemini AI
"""

import google.generativeai as genai
from typing import List, Dict
from .config import config


class TextGenerator:
    """Generate text content for e-book using Google Gemini"""
    
    def __init__(self):
        """Initialize the text generator with Gemini API"""
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_ebook_structure(self, theme: str, num_chapters: int = 5) -> Dict[str, List[str]]:
        """
        Generate the structure of the e-book including title and chapter titles
        
        Args:
            theme: The main theme/topic for the e-book
            num_chapters: Number of chapters to generate
            
        Returns:
            Dictionary with 'title' and 'chapters' (list of chapter titles)
        """
        prompt = f"""
        Você é um escritor especializado em criar e-books.
        
        Tema: {theme}
        
        Crie uma estrutura para um e-book sobre este tema com {num_chapters} capítulos.
        
        Forneça:
        1. Um título atraente para o e-book (máximo 10 palavras)
        2. {num_chapters} títulos de capítulos interessantes e relevantes
        
        Formato de resposta:
        TÍTULO: [título do e-book]
        CAPÍTULO 1: [título do capítulo 1]
        CAPÍTULO 2: [título do capítulo 2]
        ...
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        # Parse the response
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        title = ""
        chapters = []
        
        for line in lines:
            if line.startswith("TÍTULO:"):
                title = line.replace("TÍTULO:", "").strip()
            elif line.startswith("CAPÍTULO"):
                chapter_title = line.split(":", 1)[1].strip() if ":" in line else line
                chapters.append(chapter_title)
        
        return {
            "title": title or f"E-book sobre {theme}",
            "chapters": chapters if chapters else [f"Capítulo {i+1}" for i in range(num_chapters)]
        }
    
    def generate_chapter_content(self, theme: str, chapter_title: str, max_pages: int = 3) -> List[str]:
        """
        Generate content for a specific chapter
        
        Args:
            theme: The main theme of the e-book
            chapter_title: Title of the current chapter
            max_pages: Maximum number of pages to generate for this chapter
            
        Returns:
            List of page contents (one string per page)
        """
        prompt = f"""
        Você é um escritor especializado em criar e-books.
        
        Tema do e-book: {theme}
        Capítulo: {chapter_title}
        
        Escreva o conteúdo deste capítulo dividido em {max_pages} páginas.
        Cada página deve ter aproximadamente 200-300 palavras.
        
        Use uma linguagem clara, envolvente e educativa.
        
        Formato de resposta:
        [PÁGINA 1]
        [conteúdo da página 1]
        
        [PÁGINA 2]
        [conteúdo da página 2]
        
        ...
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        # Parse pages
        pages = []
        current_page = []
        
        for line in text.split('\n'):
            if line.strip().startswith('[PÁGINA') and current_page:
                pages.append('\n'.join(current_page).strip())
                current_page = []
            elif not line.strip().startswith('[PÁGINA'):
                current_page.append(line)
        
        # Add last page
        if current_page:
            pages.append('\n'.join(current_page).strip())
        
        # If parsing failed, split by paragraphs
        if not pages:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            # Group paragraphs into pages
            words_per_page = 250
            current_page_text = []
            current_word_count = 0
            
            for para in paragraphs:
                words = len(para.split())
                if current_word_count + words > words_per_page and current_page_text:
                    pages.append('\n\n'.join(current_page_text))
                    current_page_text = [para]
                    current_word_count = words
                else:
                    current_page_text.append(para)
                    current_word_count += words
            
            if current_page_text:
                pages.append('\n\n'.join(current_page_text))
        
        return pages[:max_pages] if pages else [text]
    
    def generate_image_prompt(self, theme: str, chapter_title: str, page_content: str) -> str:
        """
        Generate a descriptive prompt for image generation based on the content
        
        Args:
            theme: The main theme of the e-book
            chapter_title: Title of the current chapter
            page_content: Content of the current page
            
        Returns:
            A descriptive prompt for image generation
        """
        prompt = f"""
        Você é um especialista em criar descrições de imagens.
        
        Baseado no seguinte conteúdo de e-book:
        Tema: {theme}
        Capítulo: {chapter_title}
        Conteúdo: {page_content[:300]}...
        
        Crie uma descrição curta (máximo 50 palavras) para uma imagem ilustrativa 
        que represente visualmente este conteúdo.
        
        A descrição deve ser clara, específica e adequada para geração de imagem por IA.
        Não use formatação, apenas texto simples.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
