#!/usr/bin/env python3
"""
Script para gerar as imagens do e-book Genesis
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

# Cores pastéis
PASTEL_COLORS = {
    'rosa_claro': (255, 218, 224),
    'azul_bebe': (173, 216, 230),
    'verde_menta': (189, 252, 201),
    'amarelo_bebe': (255, 253, 208),
    'pessego': (255, 229, 180),
    'lilas': (230, 230, 250),
    'branco': (255, 255, 255),
    'lavanda': (230, 230, 250)
}

def create_pastel_gradient(width, height, color1, color2):
    """Cria um gradiente entre duas cores"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def draw_text_wrapped(draw, text, position, max_width, font, fill=(0, 0, 0)):
    """Desenha texto com quebra de linha"""
    words = text.split()
    lines = []
    current_line = []
    
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
    
    x, y = position
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + 8
    
    return y

def generate_page_1_cover(width, height):
    """Página 1 - Capa"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['lavanda'], PASTEL_COLORS['pessego'])
    draw = ImageDraw.Draw(img)
    
    # Desenhar sol sorridente
    sun_center = (width - 120, 80)
    draw.ellipse([sun_center[0]-40, sun_center[1]-40, sun_center[0]+40, sun_center[1]+40], 
                 fill=PASTEL_COLORS['amarelo_bebe'], outline=(255, 200, 100))
    # Raios do sol
    for angle in range(0, 360, 45):
        import math
        x = sun_center[0] + int(60 * math.cos(math.radians(angle)))
        y = sun_center[1] + int(60 * math.sin(math.radians(angle)))
        draw.line([sun_center, (x, y)], fill=(255, 220, 120), width=3)
    
    # Desenhar flores
    flower_positions = [(100, height-150), (200, height-120), (width-150, height-140), (width-250, height-160)]
    flower_colors = [PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['lilas'], PASTEL_COLORS['pessego'], PASTEL_COLORS['amarelo_bebe']]
    
    for pos, color in zip(flower_positions, flower_colors):
        # Pétalas
        for offset in [(0, -15), (15, 0), (0, 15), (-15, 0), (10, -10), (-10, -10), (10, 10), (-10, 10)]:
            draw.ellipse([pos[0]+offset[0]-8, pos[1]+offset[1]-8, pos[0]+offset[0]+8, pos[1]+offset[1]+8], 
                        fill=color)
        # Centro
        draw.ellipse([pos[0]-5, pos[1]-5, pos[0]+5, pos[1]+5], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Desenhar borboletas
    butterfly_pos = [(150, 200), (width-200, 250)]
    for pos in butterfly_pos:
        # Asas
        draw.ellipse([pos[0]-15, pos[1]-10, pos[0]-2, pos[1]+10], fill=PASTEL_COLORS['rosa_claro'])
        draw.ellipse([pos[0]+2, pos[1]-10, pos[0]+15, pos[1]+10], fill=PASTEL_COLORS['lilas'])
        # Corpo
        draw.ellipse([pos[0]-3, pos[1]-5, pos[0]+3, pos[1]+5], fill=(100, 100, 100))
    
    # Grama
    for x in range(0, width, 20):
        for i in range(3):
            draw.line([(x+i*5, height), (x+i*5+3, height-30)], fill=PASTEL_COLORS['verde_menta'], width=2)
    
    # Título no centro com fundo
    title_font = ImageFont.load_default()
    title = "As Maravilhosas\nHistórias de\nGênesis"
    
    # Fundo semi-transparente
    draw.rectangle([width//2-220, height//2-100, width//2+220, height//2+60], 
                  fill=(255, 255, 255, 230), outline=PASTEL_COLORS['lilas'], width=3)
    
    # Título
    y_pos = height//2 - 80
    for line in title.split('\n'):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, y_pos), line, fill=(80, 80, 120), font=title_font)
        y_pos += 30
    
    return img

def generate_page_2_creation(width, height):
    """Página 2 - Criação"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['rosa_claro'])
    draw = ImageDraw.Draw(img)
    
    # Explosão de luz no centro
    center = (width//2, height//3)
    for radius in range(150, 50, -10):
        alpha = int(255 * (1 - (radius - 50) / 100))
        color = (255, 250, 200)
        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], 
                    fill=color, outline=None)
    
    # Sol
    draw.ellipse([width-100, 60, width-40, 120], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Lua
    draw.ellipse([80, 80, 130, 130], fill=(250, 250, 250))
    
    # Estrelas
    import random
    for _ in range(20):
        x, y = random.randint(50, width-50), random.randint(50, 200)
        draw.polygon([(x, y-6), (x+2, y-2), (x+6, y), (x+2, y+2), (x, y+6), 
                     (x-2, y+2), (x-6, y), (x-2, y-2)], fill=(255, 255, 200))
    
    # Nuvens
    cloud_positions = [(150, 150), (width-200, 180), (width//2, 120)]
    for pos in cloud_positions:
        for offset in [(0, 0), (20, -5), (-20, -5), (10, 5), (-10, 5)]:
            draw.ellipse([pos[0]+offset[0]-20, pos[1]+offset[1]-15, 
                         pos[0]+offset[0]+20, pos[1]+offset[1]+15], 
                        fill=PASTEL_COLORS['branco'])
    
    # Montanhas
    draw.polygon([(0, height-150), (150, height-350), (300, height-150)], fill=PASTEL_COLORS['verde_menta'])
    draw.polygon([(200, height-150), (350, height-300), (500, height-150)], fill=(169, 242, 181))
    
    # Água
    for y in range(height-150, height, 10):
        draw.line([(0, y), (width, y)], fill=(150, 200, 230), width=8)
    
    return img

def generate_page_3_garden(width, height):
    """Página 3 - Jardim com animais"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['verde_menta'])
    draw = ImageDraw.Draw(img)
    
    # Grama
    draw.rectangle([0, height-200, width, height], fill=PASTEL_COLORS['verde_menta'])
    
    # Árvores
    tree_positions = [(100, height-300), (width-150, height-280), (width//2, height-320)]
    for pos in tree_positions:
        # Tronco
        draw.rectangle([pos[0]-15, pos[1], pos[0]+15, pos[1]+100], fill=(180, 140, 100))
        # Folhagem
        for offset in [(0, -40), (30, -20), (-30, -20), (20, 0), (-20, 0)]:
            draw.ellipse([pos[0]+offset[0]-25, pos[1]+offset[1]-25, 
                         pos[0]+offset[0]+25, pos[1]+offset[1]+25], 
                        fill=PASTEL_COLORS['verde_menta'])
    
    # Flores
    for x in range(50, width-50, 80):
        for y_offset in [0, 30]:
            flower_y = height - 150 + y_offset
            color = PASTEL_COLORS['rosa_claro'] if (x // 80) % 2 == 0 else PASTEL_COLORS['lilas']
            # Pétalas
            for offset in [(0, -10), (10, 0), (0, 10), (-10, 0)]:
                draw.ellipse([x+offset[0]-6, flower_y+offset[1]-6, x+offset[0]+6, flower_y+offset[1]+6], fill=color)
            # Centro
            draw.ellipse([x-4, flower_y-4, x+4, flower_y+4], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Coelho
    rabbit_pos = (150, height-120)
    # Corpo
    draw.ellipse([rabbit_pos[0]-20, rabbit_pos[1]-15, rabbit_pos[0]+20, rabbit_pos[1]+15], fill=(250, 250, 250))
    # Cabeça
    draw.ellipse([rabbit_pos[0]-15, rabbit_pos[1]-35, rabbit_pos[0]+15, rabbit_pos[1]-10], fill=(250, 250, 250))
    # Orelhas
    draw.ellipse([rabbit_pos[0]-12, rabbit_pos[1]-55, rabbit_pos[0]-5, rabbit_pos[1]-30], fill=PASTEL_COLORS['rosa_claro'])
    draw.ellipse([rabbit_pos[0]+5, rabbit_pos[1]-55, rabbit_pos[0]+12, rabbit_pos[1]-30], fill=PASTEL_COLORS['rosa_claro'])
    # Olhos
    draw.ellipse([rabbit_pos[0]-8, rabbit_pos[1]-28, rabbit_pos[0]-4, rabbit_pos[1]-24], fill=(50, 50, 50))
    draw.ellipse([rabbit_pos[0]+4, rabbit_pos[1]-28, rabbit_pos[0]+8, rabbit_pos[1]-24], fill=(50, 50, 50))
    
    # Borboletas
    for bx, by in [(width-150, 200), (300, 180)]:
        draw.ellipse([bx-12, by-8, bx-2, by+8], fill=PASTEL_COLORS['amarelo_bebe'])
        draw.ellipse([bx+2, by-8, bx+12, by+8], fill=PASTEL_COLORS['lilas'])
    
    # Passarinhos
    for px, py in [(width-100, 150), (200, 120)]:
        # Corpo
        draw.ellipse([px-10, py-8, px+10, py+8], fill=PASTEL_COLORS['azul_bebe'])
        # Asa
        draw.ellipse([px+5, py-5, px+15, py+5], fill=(150, 200, 230))
        # Olho
        draw.ellipse([px-5, py-3, px-2, py], fill=(50, 50, 50))
    
    return img

def generate_page_4_adam_eve(width, height):
    """Página 4 - Adão e Eva"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['pessego'])
    draw = ImageDraw.Draw(img)
    
    # Sol
    draw.ellipse([width-120, 50, width-60, 110], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Grama
    draw.rectangle([0, height-180, width, height], fill=PASTEL_COLORS['verde_menta'])
    
    # Árvore frutífera à esquerda
    draw.rectangle([80, height-400, 110, height-180], fill=(180, 140, 100))
    draw.ellipse([40, height-480, 150, height-380], fill=PASTEL_COLORS['verde_menta'])
    # Frutas (maçãs)
    for fx, fy in [(70, height-450), (100, height-430), (60, height-410)]:
        draw.ellipse([fx-8, fy-8, fx+8, fy+8], fill=(255, 150, 150))
    
    # Adão (menino - esquerda)
    adam_x, adam_y = width//2 - 60, height - 240
    # Corpo (túnica bege)
    draw.rectangle([adam_x-25, adam_y, adam_x+25, adam_y+80], fill=(245, 222, 179))
    # Cabeça
    draw.ellipse([adam_x-20, adam_y-35, adam_x+20, adam_y-5], fill=(255, 220, 177))
    # Cabelo castanho
    draw.ellipse([adam_x-22, adam_y-38, adam_x+22, adam_y-10], fill=(139, 90, 60))
    # Rosto
    draw.ellipse([adam_x-22, adam_y-32, adam_x+22, adam_y], fill=(255, 220, 177))
    # Olhos
    draw.ellipse([adam_x-12, adam_y-22, adam_x-6, adam_y-16], fill=(139, 90, 60))
    draw.ellipse([adam_x+6, adam_y-22, adam_x+12, adam_y-16], fill=(139, 90, 60))
    # Sorriso
    draw.arc([adam_x-10, adam_y-18, adam_x+10, adam_y-8], 0, 180, fill=(200, 100, 100), width=2)
    # Braços
    draw.rectangle([adam_x+25, adam_y+10, adam_x+35, adam_y+40], fill=(255, 220, 177))
    
    # Eva (menina - direita)
    eva_x, eva_y = width//2 + 60, height - 240
    # Corpo (vestido rosa)
    draw.polygon([(eva_x, eva_y), (eva_x-30, eva_y+80), (eva_x+30, eva_y+80)], fill=PASTEL_COLORS['rosa_claro'])
    # Cabeça
    draw.ellipse([eva_x-20, eva_y-35, eva_x+20, eva_y-5], fill=(255, 210, 180))
    # Cabelo castanho longo
    draw.ellipse([eva_x-22, eva_y-38, eva_x+22, eva_y+20], fill=(139, 90, 60))
    # Rosto
    draw.ellipse([eva_x-18, eva_y-32, eva_x+18, eva_y], fill=(255, 210, 180))
    # Olhos
    draw.ellipse([eva_x-12, eva_y-22, eva_x-6, eva_y-16], fill=(139, 90, 60))
    draw.ellipse([eva_x+6, eva_y-22, eva_x+12, eva_y-16], fill=(139, 90, 60))
    # Sorriso
    draw.arc([eva_x-10, eva_y-18, eva_x+10, eva_y-8], 0, 180, fill=(200, 100, 100), width=2)
    # Braço
    draw.rectangle([eva_x-35, eva_y+10, eva_x-25, eva_y+40], fill=(255, 210, 180))
    
    # Coelho aos pés
    rabbit_x, rabbit_y = width//2, height-120
    draw.ellipse([rabbit_x-15, rabbit_y-12, rabbit_x+15, rabbit_y+12], fill=(250, 250, 250))
    draw.ellipse([rabbit_x-12, rabbit_y-28, rabbit_x+12, rabbit_y-8], fill=(250, 250, 250))
    draw.ellipse([rabbit_x-10, rabbit_y-45, rabbit_x-4, rabbit_y-25], fill=PASTEL_COLORS['rosa_claro'])
    draw.ellipse([rabbit_x+4, rabbit_y-45, rabbit_x+10, rabbit_y-25], fill=PASTEL_COLORS['rosa_claro'])
    
    # Flores ao redor
    for fx in range(100, width-100, 100):
        draw.ellipse([fx-8, height-150, fx+8, height-134], fill=PASTEL_COLORS['rosa_claro'])
    
    # Passarinhos
    draw.ellipse([width-100, 180, width-80, 195], fill=PASTEL_COLORS['azul_bebe'])
    
    return img

def generate_page_5_noah_ark(width, height):
    """Página 5 - Arca de Noé"""
    img = create_pastel_gradient(width, height, (200, 200, 210), PASTEL_COLORS['azul_bebe'])
    draw = ImageDraw.Draw(img)
    
    # Chuva
    import random
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height-200)
        draw.line([(x, y), (x-2, y+15)], fill=PASTEL_COLORS['azul_bebe'], width=2)
    
    # Arca (grande barco marrom)
    ark_y = height - 350
    # Casco
    draw.polygon([(150, ark_y+100), (width-150, ark_y+100), (width-120, ark_y+200), (180, ark_y+200)], 
                fill=(160, 120, 80))
    # Estrutura superior
    draw.rectangle([200, ark_y, width-200, ark_y+100], fill=(180, 140, 100))
    # Telhado
    draw.polygon([(180, ark_y), (width//2, ark_y-40), (width-180, ark_y)], fill=(140, 100, 60))
    # Janelas
    for wx in range(250, width-250, 80):
        draw.rectangle([wx, ark_y+30, wx+40, ark_y+70], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Noé (senhor com barba branca)
    noah_x, noah_y = 250, ark_y + 40
    # Corpo (túnica marrom)
    draw.rectangle([noah_x-20, noah_y, noah_x+20, noah_y+60], fill=(160, 120, 80))
    # Cabeça
    draw.ellipse([noah_x-18, noah_y-30, noah_x+18, noah_y], fill=(255, 220, 190))
    # Cabelo e barba branca
    draw.ellipse([noah_x-20, noah_y-33, noah_x+20, noah_y+10], fill=(240, 240, 240))
    # Rosto
    draw.ellipse([noah_x-15, noah_y-28, noah_x+15, noah_y-5], fill=(255, 220, 190))
    # Olhos azuis
    draw.ellipse([noah_x-10, noah_y-22, noah_x-5, noah_y-17], fill=(135, 206, 235))
    draw.ellipse([noah_x+5, noah_y-22, noah_x+10, noah_y-17], fill=(135, 206, 235))
    
    # Animais em fila (à direita da arca)
    animals_x = width - 180
    animals_y = height - 180
    
    # Leões (amarelo claro)
    lion_y = animals_y
    draw.ellipse([animals_x-25, lion_y-15, animals_x+5, lion_y+15], fill=(255, 240, 150))  # Corpo
    draw.ellipse([animals_x-10, lion_y-10, animals_x+15, lion_y+10], fill=(255, 240, 150))  # Cabeça
    draw.ellipse([animals_x-12, lion_y-15, animals_x+17, lion_y+15], fill=(255, 220, 100))  # Juba
    
    # Girafa
    giraffe_y = animals_y - 80
    draw.rectangle([animals_x-8, giraffe_y+20, animals_x+8, giraffe_y+60], fill=(255, 235, 150))  # Corpo
    draw.rectangle([animals_x-5, giraffe_y-40, animals_x+5, giraffe_y+20], fill=(255, 235, 150))  # Pescoço
    draw.ellipse([animals_x-10, giraffe_y-50, animals_x+10, giraffe_y-35], fill=(255, 235, 150))  # Cabeça
    # Manchas
    for mx, my in [(animals_x-5, giraffe_y), (animals_x+3, giraffe_y+10), (animals_x-3, giraffe_y+30)]:
        draw.ellipse([mx-3, my-3, mx+3, my+3], fill=(200, 160, 100))
    
    # Arco-íris começando no canto
    rainbow_colors = [PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['pessego'], PASTEL_COLORS['amarelo_bebe'], 
                     PASTEL_COLORS['verde_menta'], PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['lilas']]
    for i, color in enumerate(rainbow_colors):
        draw.arc([width-250, height-350, width+50, height], 0, 90, fill=color, width=8)
        # Offset for next arc
        draw.arc([width-240+i*10, height-340, width+60+i*10, height+10], 0, 90, fill=color, width=8)
    
    return img

def generate_page_6_rainbow(width, height):
    """Página 6 - Arco-íris"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['verde_menta'])
    draw = ImageDraw.Draw(img)
    
    # Sol
    draw.ellipse([width-130, 60, width-70, 120], fill=PASTEL_COLORS['amarelo_bebe'])
    for angle in range(0, 360, 30):
        import math
        sun_x, sun_y = width-100, 90
        x = sun_x + int(50 * math.cos(math.radians(angle)))
        y = sun_y + int(50 * math.sin(math.radians(angle)))
        draw.line([sun_x, sun_y, x, y], fill=(255, 240, 150), width=3)
    
    # Grande arco-íris
    rainbow_colors = [
        PASTEL_COLORS['rosa_claro'],
        PASTEL_COLORS['pessego'],
        PASTEL_COLORS['amarelo_bebe'],
        PASTEL_COLORS['verde_menta'],
        PASTEL_COLORS['azul_bebe'],
        PASTEL_COLORS['lilas']
    ]
    
    for i, color in enumerate(rainbow_colors):
        draw.arc([-50, 100, width+50, height-50], 0, 180, fill=color, width=25)
        draw.arc([-50+i*25, 100, width+50+i*25, height-50], 0, 180, fill=color, width=25)
    
    # Terra verde com flores
    draw.rectangle([0, height-150, width, height], fill=PASTEL_COLORS['verde_menta'])
    
    # Flores brotando
    for x in range(80, width-80, 60):
        flower_colors = [PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['amarelo_bebe'], 
                        PASTEL_COLORS['lilas'], PASTEL_COLORS['pessego']]
        color = flower_colors[x % len(flower_colors)]
        flower_y = height - 100
        # Pétalas
        for offset in [(0, -8), (8, 0), (0, 8), (-8, 0)]:
            draw.ellipse([x+offset[0]-5, flower_y+offset[1]-5, x+offset[0]+5, flower_y+offset[1]+5], fill=color)
        # Centro
        draw.ellipse([x-3, flower_y-3, x+3, flower_y+3], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Arca ao fundo
    ark_x, ark_y = 150, height - 300
    draw.polygon([(ark_x, ark_y), (ark_x+150, ark_y), (ark_x+140, ark_y+80), (ark_x+10, ark_y+80)], 
                fill=(180, 140, 100))
    draw.polygon([(ark_x-10, ark_y), (ark_x+80, ark_y-30), (ark_x+170, ark_y)], fill=(140, 100, 60))
    
    # Noé com braços abertos (mesmo da página anterior)
    noah_x, noah_y = ark_x + 200, height - 250
    # Corpo
    draw.rectangle([noah_x-20, noah_y, noah_x+20, noah_y+60], fill=(160, 120, 80))
    # Braços abertos
    draw.line([noah_x-20, noah_y+20, noah_x-50, noah_y], fill=(160, 120, 80), width=8)
    draw.line([noah_x+20, noah_y+20, noah_x+50, noah_y], fill=(160, 120, 80), width=8)
    # Mãos
    draw.ellipse([noah_x-55, noah_y-5, noah_x-45, noah_y+5], fill=(255, 220, 190))
    draw.ellipse([noah_x+45, noah_y-5, noah_x+55, noah_y+5], fill=(255, 220, 190))
    # Cabeça
    draw.ellipse([noah_x-18, noah_y-30, noah_x+18, noah_y], fill=(255, 220, 190))
    # Barba branca
    draw.ellipse([noah_x-20, noah_y-33, noah_x+20, noah_y+10], fill=(240, 240, 240))
    draw.ellipse([noah_x-15, noah_y-28, noah_x+15, noah_y-5], fill=(255, 220, 190))
    # Olhos
    draw.ellipse([noah_x-10, noah_y-22, noah_x-5, noah_y-17], fill=(135, 206, 235))
    draw.ellipse([noah_x+5, noah_y-22, noah_x+10, noah_y-17], fill=(135, 206, 235))
    
    # Pomba branca voando
    dove_x, dove_y = width//2, 250
    draw.ellipse([dove_x-12, dove_y-8, dove_x+12, dove_y+8], fill=(250, 250, 250))
    # Asas
    draw.ellipse([dove_x-25, dove_y-5, dove_x-10, dove_y+10], fill=(240, 240, 240))
    draw.ellipse([dove_x+10, dove_y-5, dove_x+25, dove_y+10], fill=(240, 240, 240))
    # Raminho verde
    draw.line([dove_x+5, dove_y, dove_x+15, dove_y], fill=PASTEL_COLORS['verde_menta'], width=3)
    
    # Animais saindo
    animals_x = ark_x + 150
    animals_y = height - 200
    # Leões
    draw.ellipse([animals_x-20, animals_y-12, animals_x+10, animals_y+12], fill=(255, 240, 150))
    # Girafa ao fundo
    draw.rectangle([animals_x+30, animals_y-60, animals_x+40, animals_y], fill=(255, 235, 150))
    draw.ellipse([animals_x+27, animals_y-70, animals_x+43, animals_y-58], fill=(255, 235, 150))
    
    return img

def generate_page_7_lessons(width, height):
    """Página 7 - Lições"""
    img = Image.new('RGB', (width, height), PASTEL_COLORS['lavanda'])
    draw = ImageDraw.Draw(img)
    
    # Criar 4 quadrantes
    half_w, half_h = width//2, height//2
    
    # Quadrante 1: Criação (superior esquerdo)
    q1_img = create_pastel_gradient(half_w, half_h, PASTEL_COLORS['azul_bebe'], (200, 220, 255))
    # Sol, lua, estrelas
    q1_draw = ImageDraw.Draw(q1_img)
    q1_draw.ellipse([20, 20, 60, 60], fill=PASTEL_COLORS['amarelo_bebe'])  # Sol
    q1_draw.ellipse([half_w-60, 30, half_w-30, 60], fill=(250, 250, 250))  # Lua
    for i in range(10):
        import random
        x, y = random.randint(10, half_w-10), random.randint(10, half_h-10)
        q1_draw.polygon([(x, y-4), (x+1, y-1), (x+4, y), (x+1, y+1), 
                        (x, y+4), (x-1, y+1), (x-4, y), (x-1, y-1)], fill=(255, 255, 200))
    img.paste(q1_img, (0, 0))
    
    # Quadrante 2: Adão e Eva (superior direito)
    q2_img = create_pastel_gradient(half_w, half_h, PASTEL_COLORS['verde_menta'], PASTEL_COLORS['pessego'])
    q2_draw = ImageDraw.Draw(q2_img)
    # Adão simplificado
    adam_x, adam_y = half_w//2 - 40, half_h//2
    q2_draw.ellipse([adam_x-15, adam_y-15, adam_x+15, adam_y+15], fill=(255, 220, 177))
    q2_draw.rectangle([adam_x-20, adam_y+15, adam_x+20, adam_y+60], fill=(245, 222, 179))
    # Eva simplificada
    eva_x = half_w//2 + 40
    q2_draw.ellipse([eva_x-15, adam_y-15, eva_x+15, adam_y+15], fill=(255, 210, 180))
    q2_draw.polygon([(eva_x, adam_y+15), (eva_x-25, adam_y+60), (eva_x+25, adam_y+60)], 
                   fill=PASTEL_COLORS['rosa_claro'])
    # Flores
    for fx in [20, 60, half_w-60, half_w-20]:
        q2_draw.ellipse([fx-6, half_h-30, fx+6, half_h-18], fill=PASTEL_COLORS['rosa_claro'])
    img.paste(q2_img, (half_w, 0))
    
    # Quadrante 3: Arca (inferior esquerdo)
    q3_img = create_pastel_gradient(half_w, half_h, PASTEL_COLORS['azul_bebe'], (180, 200, 220))
    q3_draw = ImageDraw.Draw(q3_img)
    # Arca simplificada
    ark_x = half_w//2
    ark_y = half_h//2
    q3_draw.polygon([(ark_x-60, ark_y), (ark_x+60, ark_y), (ark_x+50, ark_y+50), (ark_x-50, ark_y+50)], 
                   fill=(180, 140, 100))
    q3_draw.polygon([(ark_x-65, ark_y), (ark_x, ark_y-30), (ark_x+65, ark_y)], fill=(140, 100, 60))
    # Animais pequenos
    q3_draw.ellipse([ark_x+70, ark_y+30, ark_x+85, ark_y+45], fill=(255, 240, 150))  # Leão
    q3_draw.rectangle([ark_x+90, ark_y, ark_x+95, ark_y+40], fill=(255, 235, 150))  # Girafa
    img.paste(q3_img, (0, half_h))
    
    # Quadrante 4: Arco-íris (inferior direito)
    q4_img = create_pastel_gradient(half_w, half_h, PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['verde_menta'])
    q4_draw = ImageDraw.Draw(q4_img)
    # Arco-íris
    rainbow_colors = [PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['amarelo_bebe'], 
                     PASTEL_COLORS['verde_menta'], PASTEL_COLORS['azul_bebe'], PASTEL_COLORS['lilas']]
    for i, color in enumerate(rainbow_colors):
        q4_draw.arc([10, 10, half_w-10, half_h-10], 0, 180, fill=color, width=8)
        q4_draw.arc([10+i*8, 10, half_w-10+i*8, half_h-10], 0, 180, fill=color, width=8)
    # Grama
    q4_draw.rectangle([0, half_h-30, half_w, half_h], fill=PASTEL_COLORS['verde_menta'])
    img.paste(q4_img, (half_w, half_h))
    
    # Coração grande no centro
    heart_x, heart_y = width//2, height//2
    # Desenhar coração
    heart_size = 60
    draw.ellipse([heart_x-heart_size, heart_y-heart_size//2, heart_x, heart_y+heart_size//2], 
                fill=PASTEL_COLORS['rosa_claro'])
    draw.ellipse([heart_x, heart_y-heart_size//2, heart_x+heart_size, heart_y+heart_size//2], 
                fill=PASTEL_COLORS['rosa_claro'])
    draw.polygon([(heart_x-heart_size, heart_y), (heart_x, heart_y+heart_size), 
                 (heart_x+heart_size, heart_y)], fill=PASTEL_COLORS['rosa_claro'])
    
    # Moldura
    for i in range(5):
        draw.rectangle([i*3, i*3, width-i*3, height-i*3], outline=PASTEL_COLORS['lilas'], width=2)
    
    return img

def generate_page_8_ending(width, height):
    """Página 8 - Contracapa"""
    img = create_pastel_gradient(width, height, PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['lilas'])
    draw = ImageDraw.Draw(img)
    
    # Estrelas decorativas
    import random
    for _ in range(30):
        x, y = random.randint(50, width-50), random.randint(50, height-200)
        size = random.randint(3, 6)
        draw.polygon([(x, y-size), (x+1, y-1), (x+size, y), (x+1, y+1), 
                     (x, y+size), (x-1, y+1), (x-size, y), (x-1, y-1)], 
                    fill=(255, 250, 200))
    
    # Corações pequenos
    for _ in range(15):
        x, y = random.randint(50, width-50), random.randint(50, height-200)
        size = 8
        draw.ellipse([x-size, y-size//2, x, y+size//2], fill=PASTEL_COLORS['rosa_claro'])
        draw.ellipse([x, y-size//2, x+size, y+size//2], fill=PASTEL_COLORS['rosa_claro'])
        draw.polygon([(x-size, y), (x, y+size), (x+size, y)], fill=PASTEL_COLORS['rosa_claro'])
    
    # Flores espalhadas
    for _ in range(12):
        x, y = random.randint(50, width-50), random.randint(50, height-200)
        color = random.choice([PASTEL_COLORS['amarelo_bebe'], PASTEL_COLORS['pessego'], 
                              PASTEL_COLORS['lilas']])
        for offset in [(0, -6), (6, 0), (0, 6), (-6, 0)]:
            draw.ellipse([x+offset[0]-4, y+offset[1]-4, x+offset[0]+4, y+offset[1]+4], fill=color)
        draw.ellipse([x-3, y-3, x+3, y+3], fill=PASTEL_COLORS['amarelo_bebe'])
    
    # Silhuetas de Adão e Eva na parte inferior
    silhouette_y = height - 200
    # Adão
    adam_x = width//2 - 50
    draw.ellipse([adam_x-15, silhouette_y-15, adam_x+15, silhouette_y+15], fill=(180, 160, 200))
    draw.rectangle([adam_x-20, silhouette_y+15, adam_x+20, silhouette_y+60], fill=(180, 160, 200))
    # Eva
    eva_x = width//2 + 50
    draw.ellipse([eva_x-15, silhouette_y-15, eva_x+15, silhouette_y+15], fill=(180, 160, 200))
    draw.polygon([(eva_x, silhouette_y+15), (eva_x-25, silhouette_y+60), 
                 (eva_x+25, silhouette_y+60)], fill=(180, 160, 200))
    # Mãos dadas
    draw.line([adam_x+20, silhouette_y+30, eva_x-20, silhouette_y+30], fill=(180, 160, 200), width=6)
    
    # Pomba voando acima
    dove_x, dove_y = width//2, silhouette_y - 80
    draw.ellipse([dove_x-15, dove_y-10, dove_x+15, dove_y+10], fill=(250, 250, 250))
    draw.ellipse([dove_x-30, dove_y-5, dove_x-12, dove_y+12], fill=(240, 240, 240))
    draw.ellipse([dove_x+12, dove_y-5, dove_x+30, dove_y+12], fill=(240, 240, 240))
    
    # Arco-íris pequeno no canto
    rainbow_x, rainbow_y = width - 150, 100
    rainbow_colors = [PASTEL_COLORS['rosa_claro'], PASTEL_COLORS['amarelo_bebe'], 
                     PASTEL_COLORS['verde_menta'], PASTEL_COLORS['azul_bebe']]
    for i, color in enumerate(rainbow_colors):
        draw.arc([rainbow_x, rainbow_y, rainbow_x+100, rainbow_y+50], 0, 180, fill=color, width=5)
        draw.arc([rainbow_x+i*5, rainbow_y, rainbow_x+100+i*5, rainbow_y+50], 0, 180, fill=color, width=5)
    
    return img

# Gerar todas as páginas
width, height = 800, 1200
output_dir = "output/as_maravilhosas_historias_de_genesis"

pages = [
    ("page_001_cover.png", generate_page_1_cover),
    ("page_002_creation.png", generate_page_2_creation),
    ("page_003_garden.png", generate_page_3_garden),
    ("page_004_adam_eve.png", generate_page_4_adam_eve),
    ("page_005_noah_ark.png", generate_page_5_noah_ark),
    ("page_006_rainbow.png", generate_page_6_rainbow),
    ("page_007_lessons.png", generate_page_7_lessons),
    ("page_008_ending.png", generate_page_8_ending)
]

print("🎨 Gerando imagens do e-book...")
for filename, generator_func in pages:
    print(f"   Gerando {filename}...")
    img = generator_func(width, height)
    img.save(os.path.join(output_dir, filename))
    print(f"   ✅ {filename} salva!")

print("\n✨ Todas as imagens foram geradas com sucesso!")
print(f"📁 Localização: {output_dir}/")
