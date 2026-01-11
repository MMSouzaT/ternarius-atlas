#!/usr/bin/env python3
"""
Gerador de imagens com Stable Diffusion
Otimizado para NVIDIA RTX 3050 (8GB VRAM)
"""

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import json
import os
import sys
import time

# Configurações otimizadas para RTX 3050
CONFIG = {
    "model": "runwayml/stable-diffusion-v1-5",  # Modelo rápido e eficiente
    "num_inference_steps": 30,  # 30 = rápido, 50 = melhor qualidade
    "guidance_scale": 7.5,
    "width": 800,
    "height": 1200,
    "negative_prompt": "ugly, blurry, low quality, distorted, deformed, text, watermark, signature",
}


def check_gpu():
    """Verifica se GPU está disponível"""
    print("=" * 70)
    print("VERIFICANDO GPU")
    print("=" * 70)
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        print("\n✅ GPU pronta para usar!")
        return True
    else:
        print("\n⚠️  GPU não encontrada. Usando CPU (será muito mais lento)")
        response = input("Continuar mesmo assim? (s/n): ").strip().lower()
        return response in ['s', 'sim', 'y', 'yes']


def load_pipeline():
    """Carrega o pipeline do Stable Diffusion"""
    print("\n" + "=" * 70)
    print("CARREGANDO STABLE DIFFUSION")
    print("=" * 70)
    print(f"Modelo: {CONFIG['model']}")
    print("⏳ Primeira vez pode demorar (baixando modelo ~4GB)...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        # Carregar pipeline
        pipe = StableDiffusionPipeline.from_pretrained(
            CONFIG['model'],
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,  # Remover safety checker para velocidade
        )
        
        # Usar scheduler otimizado
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        pipe = pipe.to(device)
        
        # Otimizações para RTX 3050 (8GB VRAM)
        if device == "cuda":
            print("\n🔧 Aplicando otimizações para GPU...")
            
            # Ativar xformers se disponível (muito mais rápido)
            try:
                pipe.enable_xformers_memory_efficient_attention()
                print("   ✅ xformers ativado")
            except:
                print("   ⚠️  xformers não disponível (instale com: pip install xformers)")
            
            # Ativar attention slicing (economiza VRAM)
            pipe.enable_attention_slicing(1)
            print("   ✅ Attention slicing ativado")
            
            # Ativar VAE slicing (economiza mais VRAM)
            pipe.enable_vae_slicing()
            print("   ✅ VAE slicing ativado")
        
        print("\n✅ Pipeline carregado com sucesso!")
        return pipe
    
    except Exception as e:
        print(f"\n❌ Erro ao carregar pipeline: {e}")
        return None


def generate_image(pipe, prompt, negative_prompt=None, seed=None):
    """Gera uma imagem com Stable Diffusion"""
    
    if seed is not None:
        generator = torch.Generator("cuda" if torch.cuda.is_available() else "cpu").manual_seed(seed)
    else:
        generator = None
    
    start_time = time.time()
    
    with torch.inference_mode():
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt or CONFIG['negative_prompt'],
            num_inference_steps=CONFIG['num_inference_steps'],
            guidance_scale=CONFIG['guidance_scale'],
            width=CONFIG['width'],
            height=CONFIG['height'],
            generator=generator,
        ).images[0]
    
    elapsed = time.time() - start_time
    
    return image, elapsed


def generate_from_structure(structure_path, output_folder):
    """Gera imagens baseado na estrutura JSON"""
    
    # Carregar estrutura
    with open(structure_path, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    print("\n" + "=" * 70)
    print(f"GERANDO IMAGENS PARA: {structure['title']}")
    print("=" * 70)
    print(f"Total de páginas: {len(structure['pages'])}")
    print(f"Pasta de saída: {output_folder}")
    
    # Criar pasta se não existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Carregar pipeline
    pipe = load_pipeline()
    if pipe is None:
        return False
    
    print("\n" + "=" * 70)
    print("GERANDO IMAGENS")
    print("=" * 70)
    
    total_time = 0
    
    for i, page in enumerate(structure['pages'], 1):
        print(f"\n📄 Página {i}/{len(structure['pages'])}")
        print(f"   Tipo: {page['type']}")
        
        # Melhorar prompt para estilo infantil com tons pastéis
        enhanced_prompt = f"Children's book illustration, soft pastel colors, watercolor style, gentle and calm, {page['illustration_description']}"
        
        print(f"   Prompt: {enhanced_prompt[:80]}...")
        
        # Gerar imagem
        print(f"   🎨 Gerando... ", end='', flush=True)
        image, elapsed = generate_image(pipe, enhanced_prompt, seed=42+i)
        total_time += elapsed
        
        print(f"[{elapsed:.1f}s]")
        
        # Salvar
        filename = f"page_{i:03d}_sd.png"
        filepath = os.path.join(output_folder, filename)
        image.save(filepath)
        
        print(f"   ✅ Salva: {filename}")
    
    avg_time = total_time / len(structure['pages'])
    
    print("\n" + "=" * 70)
    print("✨ GERAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print(f"✅ {len(structure['pages'])} imagens geradas")
    print(f"⏱️  Tempo total: {total_time:.1f}s")
    print(f"⏱️  Tempo médio por imagem: {avg_time:.1f}s")
    print(f"📁 Localização: {output_folder}/")
    
    return True


def main():
    """Função principal"""
    
    # Verificar GPU
    if not check_gpu():
        print("\n❌ Operação cancelada.")
        return 1
    
    # Verificar se tem estrutura do Genesis
    default_structure = "output/as_maravilhosas_historias_de_genesis/structure.json"
    
    if os.path.exists(default_structure):
        print(f"\n📚 Estrutura encontrada: {default_structure}")
        response = input("Deseja gerar imagens para este e-book? (s/n): ").strip().lower()
        
        if response in ['s', 'sim', 'y', 'yes']:
            output_folder = "output/as_maravilhosas_historias_de_genesis"
            success = generate_from_structure(default_structure, output_folder)
            return 0 if success else 1
    
    # Modo manual
    print("\n📝 Modo manual:")
    prompt = input("Digite a descrição da imagem: ").strip()
    
    if not prompt:
        print("❌ Prompt vazio.")
        return 1
    
    pipe = load_pipeline()
    if pipe is None:
        return 1
    
    print("\n🎨 Gerando imagem...")
    image, elapsed = generate_image(pipe, prompt)
    
    filename = "output_sd.png"
    image.save(filename)
    
    print(f"\n✅ Imagem gerada em {elapsed:.1f}s")
    print(f"📁 Salva em: {filename}")
    
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
