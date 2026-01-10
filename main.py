#!/usr/bin/env python3
"""
Main script to run Ternarius Atlas E-book Generator
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ternarius_atlas import EbookGenerator


def main():
    """Main function to run the e-book generator"""
    
    print("=" * 60)
    print("🌟 Bem-vindo ao Ternarius Atlas - Gerador de E-books com IA 🌟")
    print("=" * 60)
    
    # Get theme from user
    if len(sys.argv) > 1:
        theme = ' '.join(sys.argv[1:])
    else:
        theme = input("\n📝 Digite o tema do e-book que você deseja gerar: ").strip()
        
        if not theme:
            print("❌ Erro: Tema não pode ser vazio!")
            return 1
    
    print(f"\n🎯 Tema escolhido: {theme}")
    
    # Ask for customization
    print("\n⚙️  Configurações:")
    try:
        num_chapters = input("   Número de capítulos (padrão: 3): ").strip()
        num_chapters = int(num_chapters) if num_chapters else 3
        
        pages_per_chapter = input("   Páginas por capítulo (padrão: 2): ").strip()
        pages_per_chapter = int(pages_per_chapter) if pages_per_chapter else 2
        
        include_images_input = input("   Incluir imagens ilustrativas? (s/n, padrão: s): ").strip().lower()
        include_images = include_images_input != 'n'
    except ValueError:
        print("⚠️  Valor inválido, usando configurações padrão...")
        num_chapters = 3
        pages_per_chapter = 2
        include_images = True
    except KeyboardInterrupt:
        print("\n\n👋 Operação cancelada pelo usuário.")
        return 0
    
    try:
        # Initialize generator
        generator = EbookGenerator(output_dir="output")
        
        # Generate e-book
        pages = generator.generate_ebook(
            theme=theme,
            num_chapters=num_chapters,
            pages_per_chapter=pages_per_chapter,
            include_images=include_images
        )
        
        print(f"\n✅ Sucesso! {len(pages)} páginas geradas.")
        print(f"📁 Verifique o diretório 'output' para ver seu e-book!")
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ Erro de configuração: {e}")
        print("💡 Dica: Certifique-se de que o arquivo .env está configurado corretamente.")
        print("   Copie .env.example para .env e adicione sua chave da API do Gemini.")
        return 1
    except Exception as e:
        print(f"\n❌ Erro ao gerar e-book: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
