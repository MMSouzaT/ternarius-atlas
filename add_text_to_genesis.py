#!/usr/bin/env python3
"""
Script para adicionar textos às imagens do e-book Genesis
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

def add_text_to_image(base_image, text, page_number):
    """Adiciona texto a uma imagem de forma legível"""
    result = base_image.copy().convert('RGBA')
    width, height = result.size
    
    # Criar overlay com texto
    overlay = Image.new('RGBA', result.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Área de texto na parte inferior (35% da imagem)
    text_area_height = int(height * 0.35)
    text_area_y = height - text_area_height
    
    # Fundo semi-transparente branco para o texto
    overlay_draw.rectangle(
        [(0, text_area_y), (width, height)],
        fill=(255, 255, 255, 220)
    )
    
    # Composite overlay
    result = Image.alpha_composite(result, overlay).convert('RGB')
    draw = ImageDraw.Draw(result)
    
    # Fonte
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Quebrar texto em linhas
    words = text.split()
    lines = []
    current_line = []
    padding = 30
    max_width = width - 2 * padding
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Desenhar texto
    y_pos = text_area_y + padding
    bbox = draw.textbbox((0, 0), "Ay", font=font)
    line_height = int((bbox[3] - bbox[1]) * 1.5)
    
    # Limitar número de linhas
    max_lines = (text_area_height - 2 * padding - 30) // line_height
    
    for i, line in enumerate(lines):
        if i >= max_lines:
            if i == max_lines:
                draw.text((padding, y_pos), "...", fill=(50, 50, 50), font=font)
            break
        
        draw.text((padding, y_pos), line, fill=(30, 30, 30), font=font)
        y_pos += line_height
    
    # Número da página
    page_num_text = f"— {page_number} —"
    bbox = draw.textbbox((0, 0), page_num_text, font=font)
    text_width = bbox[2] - bbox[0]
    page_num_x = (width - text_width) // 2
    page_num_y = height - padding + 5
    draw.text((page_num_x, page_num_y), page_num_text, fill=(100, 100, 100), font=font)
    
    return result

def add_title_to_cover(base_image, title):
    """Adiciona título à capa (imagem já tem o título, então retorna como está)"""
    return base_image

# Carregar estrutura
output_dir = "output/as_maravilhosas_historias_de_genesis"
with open(os.path.join(output_dir, "structure.json"), 'r', encoding='utf-8') as f:
    structure = json.load(f)

print("📝 Adicionando textos às imagens...")

for i, page in enumerate(structure['pages'], 1):
    print(f"\n📄 Processando página {i}/{len(structure['pages'])}...")
    
    # Nome do arquivo base
    base_filename = f"page_{i:03d}_"
    
    # Encontrar arquivo de imagem correspondente
    image_files = [f for f in os.listdir(output_dir) if f.startswith(base_filename) and not f.endswith('_final.png')]
    
    if not image_files:
        print(f"   ⚠️  Imagem não encontrada para página {i}")
        continue
    
    image_path = os.path.join(output_dir, image_files[0])
    base_image = Image.open(image_path)
    
    # Adicionar texto
    if page['type'] == 'cover':
        # Capa já tem título desenhado
        final_image = add_title_to_cover(base_image, page['title'])
    else:
        # Juntar título e texto
        full_text = ""
        if page.get('title'):
            full_text = f"{page['title']}\n\n"
        full_text += page.get('text', '')
        
        final_image = add_text_to_image(base_image, full_text, i)
    
    # Salvar imagem final
    final_filename = f"page_{i:03d}_final.png"
    final_path = os.path.join(output_dir, final_filename)
    final_image.save(final_path)
    
    print(f"   ✅ Salva: {final_filename}")

print("\n" + "=" * 70)
print("🎉 E-BOOK COMPLETO!")
print("=" * 70)
print(f"✅ {len(structure['pages'])} páginas finais geradas!")
print(f"📁 Localização: {output_dir}/")
print(f"\n📚 Arquivos finais:")
for i in range(1, len(structure['pages']) + 1):
    print(f"   • page_{i:03d}_final.png")

print("\n✨ Processo concluído com sucesso! ✨")
