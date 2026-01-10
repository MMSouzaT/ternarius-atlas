#!/usr/bin/env python3
"""
Example script demonstrating how to use Ternarius Atlas programmatically
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ternarius_atlas import EbookGenerator


def example_basic():
    """Basic example of e-book generation"""
    print("Exemplo 1: Geração Básica de E-book")
    print("-" * 60)
    
    # Create generator
    generator = EbookGenerator(output_dir="output/example_basic")
    
    # Generate a quick demo e-book
    pages = generator.generate_quick_ebook(theme="Inteligência Artificial")
    
    print(f"\nE-book gerado com {len(pages)} páginas!")


def example_custom():
    """Example with custom configuration"""
    print("\nExemplo 2: Geração com Configuração Personalizada")
    print("-" * 60)
    
    # Create generator with custom output directory
    generator = EbookGenerator(output_dir="output/example_custom")
    
    # Generate e-book with custom settings
    pages = generator.generate_ebook(
        theme="História da Programação",
        num_chapters=4,
        pages_per_chapter=3,
        include_images=True,
        author="Ternarius Atlas AI"
    )
    
    print(f"\nE-book personalizado gerado com {len(pages)} páginas!")


def example_no_images():
    """Example without images (faster generation)"""
    print("\nExemplo 3: Geração Sem Imagens (Mais Rápido)")
    print("-" * 60)
    
    generator = EbookGenerator(output_dir="output/example_text_only")
    
    pages = generator.generate_ebook(
        theme="Fundamentos de Python",
        num_chapters=3,
        pages_per_chapter=2,
        include_images=False
    )
    
    print(f"\nE-book (apenas texto) gerado com {len(pages)} páginas!")


if __name__ == "__main__":
    try:
        # Run examples
        example_basic()
        
        # Uncomment to run other examples:
        # example_custom()
        # example_no_images()
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Certifique-se de:")
        print("   1. Copiar .env.example para .env")
        print("   2. Adicionar sua chave da API do Google Gemini no arquivo .env")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
