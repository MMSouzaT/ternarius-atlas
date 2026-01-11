#!/usr/bin/env python3
"""
Main script to run Ternarius Atlas E-book Generator - Interactive Mode
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ternarius_atlas import EbookGenerator
from ternarius_atlas.text_generator import TextGenerator
from ternarius_atlas.image_generator import ImageGenerator
from ternarius_atlas.page_composer import PageComposer
from ternarius_atlas.config import config
from PIL import Image


class InteractiveEbookGenerator:
    """Interactive e-book generator with step-by-step confirmation"""
    
    def __init__(self):
        self.text_generator = TextGenerator()
        self.image_generator = ImageGenerator()
        self.page_composer = PageComposer(config)
        self.book_structure = None
        self.book_title = None
        self.output_folder = None
        
    def sanitize_folder_name(self, title: str) -> str:
        """Convert book title to valid folder name"""
        # Remove special characters and replace spaces with underscores
        sanitized = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
        sanitized = sanitized.replace(' ', '_').lower()
        return sanitized[:50]  # Limit length
    
    def step1_generate_structure(self, theme: str, instructions: str = ""):
        """Step 1: Generate book structure and get user approval"""
        print("\n" + "=" * 70)
        print("📋 ETAPA 1: GERAÇÃO DA ESTRUTURA DO LIVRO")
        print("=" * 70)
        print(f"🎯 Tema: {theme}")
        if instructions:
            print(f"📝 Instruções adicionais: {instructions}")
        print("\n⏳ Gerando estrutura do livro com IA...")
        
        # Generate structure using AI
        full_prompt = f"{theme}\n\nInstruções adicionais: {instructions}" if instructions else theme
        structure = self.text_generator.generate_detailed_ebook_structure(full_prompt)
        
        self.book_structure = structure
        self.book_title = structure['title']
        
        # Display structure to user
        print("\n" + "=" * 70)
        print("📚 ESTRUTURA PROPOSTA DO LIVRO")
        print("=" * 70)
        print(f"\n📖 Título: {structure['title']}")
        print(f"📄 Total de páginas: {structure['total_pages']}")
        print(f"\n📝 Descrição: {structure['description']}")
        
        print(f"\n📑 PÁGINAS ({len(structure['pages'])} páginas):")
        print("-" * 70)
        
        for i, page in enumerate(structure['pages'], 1):
            print(f"\n📄 Página {i}:")
            print(f"   🏷️  Tipo: {page['type']}")
            if page['type'] == 'cover':
                print(f"   📖 Título: {page['title']}")
                print(f"   🎨 Ilustração: {page['illustration_description']}")
            elif page['type'] in ['chapter', 'content']:
                if 'title' in page:
                    print(f"   📖 Título: {page['title']}")
                print(f"   📝 Texto: {page['text'][:100]}{'...' if len(page['text']) > 100 else ''}")
                print(f"   🎨 Ilustração: {page['illustration_description']}")
        
        print("\n" + "=" * 70)
        
        # Get user approval
        while True:
            response = input("\n✅ Está de acordo com essa estrutura? (s/n): ").strip().lower()
            if response in ['s', 'sim', 'yes', 'y']:
                # Create output folder
                folder_name = self.sanitize_folder_name(self.book_title)
                self.output_folder = os.path.join('output', folder_name)
                os.makedirs(self.output_folder, exist_ok=True)
                
                # Save structure to JSON
                structure_path = os.path.join(self.output_folder, 'structure.json')
                with open(structure_path, 'w', encoding='utf-8') as f:
                    json.dump(structure, f, ensure_ascii=False, indent=2)
                
                print(f"\n✅ Estrutura aprovada! Pasta criada: {self.output_folder}")
                return True
            elif response in ['n', 'nao', 'não', 'no']:
                print("\n❌ Estrutura rejeitada. Por favor, execute novamente com instruções diferentes.")
                return False
            else:
                print("⚠️  Por favor, responda 's' para sim ou 'n' para não.")
    
    def step2_generate_images(self):
        """Step 2: Generate all images without text"""
        if not self.book_structure:
            print("❌ Erro: Execute a Etapa 1 primeiro!")
            return False
        
        print("\n" + "=" * 70)
        print("🎨 ETAPA 2: GERAÇÃO DAS IMAGENS")
        print("=" * 70)
        print(f"📊 Gerando {len(self.book_structure['pages'])} imagens...")
        
        self.book_structure['images'] = []
        
        for i, page in enumerate(self.book_structure['pages'], 1):
            print(f"\n🎨 Gerando imagem {i}/{len(self.book_structure['pages'])}...")
            print(f"   📝 Descrição: {page['illustration_description'][:80]}...")
            
            # Generate image
            image = self.image_generator.generate_image(
                page['illustration_description'],
                width=config.DEFAULT_PAGE_WIDTH,
                height=config.DEFAULT_PAGE_HEIGHT
            )
            
            # Save image
            image_filename = f"image_{i:03d}.png"
            image_path = os.path.join(self.output_folder, image_filename)
            image.save(image_path)
            
            self.book_structure['images'].append(image_path)
            print(f"   ✅ Salva: {image_filename}")
        
        print("\n" + "=" * 70)
        print(f"✅ Todas as {len(self.book_structure['images'])} imagens foram geradas!")
        print(f"📁 Localização: {self.output_folder}/")
        
        # Get user approval
        while True:
            response = input("\n✅ As imagens estão boas ou deseja alterar alguma? (boas/alterar): ").strip().lower()
            if response in ['boas', 'b', 'boa', 'sim', 's', 'yes', 'y']:
                print("\n✅ Imagens aprovadas!")
                return True
            elif response in ['alterar', 'a', 'modificar', 'm', 'nao', 'não', 'n', 'no']:
                page_num = input("   Qual número da página deseja alterar? (ou 'cancelar'): ").strip()
                if page_num.lower() in ['cancelar', 'cancel', 'c']:
                    continue
                try:
                    page_idx = int(page_num) - 1
                    if 0 <= page_idx < len(self.book_structure['pages']):
                        new_description = input(f"   Nova descrição da ilustração: ").strip()
                        if new_description:
                            self.book_structure['pages'][page_idx]['illustration_description'] = new_description
                            print(f"\n🎨 Regenerando imagem {page_num}...")
                            
                            image = self.image_generator.generate_image(
                                new_description,
                                width=config.DEFAULT_PAGE_WIDTH,
                                height=config.DEFAULT_PAGE_HEIGHT
                            )
                            image_path = self.book_structure['images'][page_idx]
                            image.save(image_path)
                            print(f"   ✅ Imagem {page_num} atualizada!")
                    else:
                        print(f"   ⚠️  Número de página inválido. Escolha entre 1 e {len(self.book_structure['pages'])}")
                except ValueError:
                    print("   ⚠️  Número inválido.")
            else:
                print("⚠️  Por favor, responda 'boas' ou 'alterar'.")
    
    def step3_add_text_to_images(self):
        """Step 3: Add text to images"""
        if not self.book_structure or not self.book_structure.get('images'):
            print("❌ Erro: Execute as Etapas 1 e 2 primeiro!")
            return False
        
        print("\n" + "=" * 70)
        print("📝 ETAPA 3: ADICIONANDO TEXTO ÀS IMAGENS")
        print("=" * 70)
        print(f"📊 Processando {len(self.book_structure['pages'])} páginas...")
        
        final_pages = []
        
        for i, page in enumerate(self.book_structure['pages'], 1):
            print(f"\n📝 Processando página {i}/{len(self.book_structure['pages'])}...")
            
            # Load base image
            image_path = self.book_structure['images'][i-1]
            base_image = Image.open(image_path)
            
            # Add text to image
            if page['type'] == 'cover':
                final_image = self.page_composer.add_text_to_cover(
                    base_image,
                    page['title']
                )
            else:
                text = page.get('title', '')
                if 'text' in page:
                    text = f"{text}\n\n{page['text']}" if text else page['text']
                
                final_image = self.page_composer.add_text_to_page(
                    base_image,
                    text,
                    page_number=i
                )
            
            # Save final page
            final_filename = f"page_{i:03d}_final.png"
            final_path = os.path.join(self.output_folder, final_filename)
            final_image.save(final_path)
            final_pages.append(final_path)
            
            print(f"   ✅ Salva: {final_filename}")
        
        print("\n" + "=" * 70)
        print("🎉 E-BOOK COMPLETO!")
        print("=" * 70)
        print(f"✅ {len(final_pages)} páginas finais geradas!")
        print(f"📁 Localização: {self.output_folder}/")
        print(f"📚 Arquivos:")
        for page in final_pages:
            print(f"   • {os.path.basename(page)}")
        
        return True


def main():
    """Main function to run the interactive e-book generator"""
    
    print("=" * 70)
    print("🌟 Bem-vindo ao Ternarius Atlas - Gerador de E-books com IA 🌟")
    print("=" * 70)
    print("\n📖 Sistema Interativo de Geração de E-books")
    print("   Processo em 3 etapas com confirmação em cada passo\n")
    
    # Get theme and instructions from user
    theme = input("📝 Digite o tema do e-book: ").strip()
    
    if not theme:
        print("❌ Erro: Tema não pode ser vazio!")
        return 1
    
    instructions = input("📋 Instruções adicionais (opcional, Enter para pular): ").strip()
    
    # Create interactive generator
    generator = InteractiveEbookGenerator()
    
    # Step 1: Generate and approve structure
    if not generator.step1_generate_structure(theme, instructions):
        return 1
    
    # Step 2: Generate and approve images
    if not generator.step2_generate_images():
        return 1
    
    # Step 3: Add text to images
    if not generator.step3_add_text_to_images():
        return 1
    
    print("\n" + "=" * 70)
    print("✨ Processo concluído com sucesso! ✨")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
