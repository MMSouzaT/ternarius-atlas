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
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
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
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
        except Exception as e:
            print(f"Erro ao gerar estrutura do e-book: {e}")
            # Return default structure on error
            return {
                "title": f"E-book sobre {theme}",
                "chapters": [f"Capítulo {i+1}: Introdução ao tema" for i in range(num_chapters)]
            }
        
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
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
        except Exception as e:
            print(f"Erro ao gerar conteúdo do capítulo: {e}")
            # Return default content on error
            text = f"""Este é o capítulo sobre {chapter_title}.
            
            O conteúdo está relacionado ao tema {theme} e fornece 
            informações importantes sobre este tópico.
            
            [Conteúdo gerado com erro - verifique sua conexão e API key]"""
        
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
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Erro ao gerar prompt de imagem: {e}")
            # Return a simple default prompt
            return f"Ilustração sobre {chapter_title} relacionada ao tema {theme}"
    
    def generate_detailed_ebook_structure(self, theme: str) -> dict:
        """
        Generate a detailed e-book structure with all pages, texts and illustration descriptions
        
        Args:
            theme: The main theme/topic for the e-book with optional instructions
            
        Returns:
            Dictionary with complete book structure including all pages
        """
        prompt = f"""
        Você é um especialista em criar e-books educativos e envolventes.
        
        Tema/Instruções: {theme}
        
        Crie uma estrutura COMPLETA para um e-book com as seguintes informações:
        
        1. Título atraente do e-book (máximo 8 palavras)
        2. Breve descrição do livro (1-2 frases)
        3. Número total de páginas (recomendado: 6-10 páginas)
        4. Para CADA página do livro, forneça:
           - Tipo da página (cover/chapter/content)
           - Título (se aplicável)
           - Texto completo da página (2-4 parágrafos curtos, linguagem simples e clara)
           - Descrição detalhada da ilustração (50-80 palavras, específica para geração de imagem por IA)
        
        FORMATO DE RESPOSTA (siga EXATAMENTE este formato):
        
        TÍTULO: [título do e-book]
        DESCRIÇÃO: [descrição breve]
        TOTAL_PÁGINAS: [número]
        
        ---PÁGINA 1---
        TIPO: cover
        TÍTULO: [título para a capa]
        TEXTO: [deixar vazio para capa]
        ILUSTRAÇÃO: [descrição detalhada da imagem de capa, incluindo estilo artístico, cores, elementos visuais]
        
        ---PÁGINA 2---
        TIPO: chapter
        TÍTULO: [título do capítulo]
        TEXTO: [texto completo desta página, 2-4 parágrafos]
        ILUSTRAÇÃO: [descrição detalhada da imagem]
        
        ---PÁGINA 3---
        TIPO: content
        TÍTULO: [subtítulo ou deixar vazio]
        TEXTO: [texto completo desta página]
        ILUSTRAÇÃO: [descrição detalhada da imagem]
        
        [Continue para todas as páginas...]
        
        IMPORTANTE:
        - Use linguagem adequada para o público-alvo
        - Textos devem ser concisos e claros
        - Descrições de ilustrações devem ser específicas e visuais
        - Inclua variedade visual nas ilustrações
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
        except Exception as e:
            print(f"Erro ao gerar estrutura do e-book: {e}")
            # Return a default structure
            return {
                'title': 'Livro sobre ' + theme[:30],
                'description': 'Um livro gerado automaticamente',
                'total_pages': 5,
                'pages': [
                    {
                        'type': 'cover',
                        'title': 'Livro sobre ' + theme[:30],
                        'text': '',
                        'illustration_description': 'Capa colorida e atraente sobre ' + theme[:50]
                    },
                    {
                        'type': 'content',
                        'title': 'Capítulo 1',
                        'text': 'Conteúdo sobre o tema.',
                        'illustration_description': 'Ilustração relacionada ao tema'
                    }
                ]
            }
        
        # Parse the structured response
        return self._parse_ebook_structure(text)
    
    def _parse_ebook_structure(self, text: str) -> dict:
        """Parse the AI-generated structure into a dictionary"""
        structure = {
            'title': '',
            'description': '',
            'total_pages': 0,
            'pages': []
        }
        
        lines = text.split('\n')
        current_page = None
        current_field = None
        
        for line in lines:
            line = line.strip()
            
            # Parse header info
            if line.startswith('TÍTULO:'):
                structure['title'] = line.replace('TÍTULO:', '').strip()
            elif line.startswith('DESCRIÇÃO:'):
                structure['description'] = line.replace('DESCRIÇÃO:', '').strip()
            elif line.startswith('TOTAL_PÁGINAS:'):
                try:
                    structure['total_pages'] = int(line.replace('TOTAL_PÁGINAS:', '').strip())
                except:
                    pass
            
            # Parse page sections
            elif line.startswith('---PÁGINA'):
                if current_page:
                    structure['pages'].append(current_page)
                current_page = {
                    'type': 'content',
                    'title': '',
                    'text': '',
                    'illustration_description': ''
                }
                current_field = None
            
            elif current_page is not None:
                if line.startswith('TIPO:'):
                    current_page['type'] = line.replace('TIPO:', '').strip().lower()
                    current_field = None
                elif line.startswith('TÍTULO:'):
                    current_page['title'] = line.replace('TÍTULO:', '').strip()
                    current_field = None
                elif line.startswith('TEXTO:'):
                    text_content = line.replace('TEXTO:', '').strip()
                    if text_content:
                        current_page['text'] = text_content
                    current_field = 'text'
                elif line.startswith('ILUSTRAÇÃO:'):
                    illust_content = line.replace('ILUSTRAÇÃO:', '').strip()
                    if illust_content:
                        current_page['illustration_description'] = illust_content
                    current_field = 'illustration'
                elif line and current_field:
                    # Continue multiline content
                    if current_field == 'text':
                        current_page['text'] += ' ' + line
                    elif current_field == 'illustration':
                        current_page['illustration_description'] += ' ' + line
        
        # Add last page
        if current_page:
            structure['pages'].append(current_page)
        
        # Set total pages if not provided
        if structure['total_pages'] == 0:
            structure['total_pages'] = len(structure['pages'])
        
        # Ensure we have at least a basic structure
        if not structure['pages']:
            structure['pages'] = [{
                'type': 'cover',
                'title': structure['title'] or 'Meu Livro',
                'text': '',
                'illustration_description': 'Uma capa bonita e colorida'
            }]
        
        return structure
