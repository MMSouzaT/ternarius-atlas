#!/usr/bin/env python3
"""
Gerador de imagens usando Stable Diffusion
"""

import torch
from diffusers import StableDiffusionPipeline
import os
from pathlib import Path

class StableDiffusionImageGenerator:
    """Gerador de imagens usando Stable Diffusion"""
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", use_cpu=True):
        """
        Inicializa o gerador Stable Diffusion
        
        Args:
            model_id: ID do modelo no Hugging Face
            use_cpu: Se True, usa CPU (mais lento mas funciona sem GPU)
        """
        print(f"🔧 Carregando modelo Stable Diffusion: {model_id}")
        print("   ⚠️  Primeira execução vai baixar ~5GB de dados...")
        
        # Configurar device
        if use_cpu:
            self.device = "cpu"
            torch_dtype = torch.float32
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        print(f"   🖥️  Usando: {self.device.upper()}")
        
        # Carregar pipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            safety_checker=None,  # Desabilitar para imagens infantis
            requires_safety_checker=False
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # Otimizações para CPU
        if use_cpu:
            # Reduzir uso de memória
            self.pipe.enable_attention_slicing()
        
        print("   ✅ Modelo carregado!")
    
    def generate_image(self, prompt, negative_prompt="", width=512, height=512, num_inference_steps=25):
        """
        Gera uma imagem a partir de um prompt
        
        Args:
            prompt: Descrição da imagem desejada
            negative_prompt: Coisas a evitar na imagem
            width: Largura da imagem (múltiplo de 8)
            height: Altura da imagem (múltiplo de 8)
            num_inference_steps: Número de steps (mais = melhor qualidade, mais lento)
        
        Returns:
            PIL Image
        """
        # Garantir múltiplos de 8
        width = (width // 8) * 8
        height = (height // 8) * 8
        
        # Prompt otimizado para ilustrações infantis
        enhanced_prompt = f"{prompt}, children's book illustration, soft pastel colors, cute style, watercolor, gentle, warm, friendly"
        
        # Negative prompt padrão
        default_negative = "ugly, blurry, bad anatomy, dark, scary, violent, realistic photo, adult content"
        full_negative = f"{negative_prompt}, {default_negative}" if negative_prompt else default_negative
        
        print(f"\n🎨 Gerando imagem...")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Tamanho: {width}x{height}")
        print(f"   Steps: {num_inference_steps}")
        
        # Gerar imagem
        with torch.no_grad():
            result = self.pipe(
                enhanced_prompt,
                negative_prompt=full_negative,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=7.5
            )
        
        return result.images[0]
    
    def generate_batch(self, prompts, output_dir, **kwargs):
        """
        Gera múltiplas imagens em lote
        
        Args:
            prompts: Lista de prompts
            output_dir: Diretório para salvar
            **kwargs: Argumentos para generate_image
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        images = []
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📄 Imagem {i}/{len(prompts)}")
            image = self.generate_image(prompt, **kwargs)
            
            # Salvar
            filename = f"image_{i:03d}.png"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath)
            images.append(filepath)
            print(f"   ✅ Salva: {filename}")
        
        return images


def test_generator():
    """Teste rápido do gerador"""
    print("=" * 70)
    print("🧪 TESTE DO STABLE DIFFUSION")
    print("=" * 70)
    
    # Criar gerador
    generator = StableDiffusionImageGenerator(use_cpu=True)
    
    # Teste com prompt simples
    test_prompt = "a cute cartoon rabbit in a garden with flowers, pastel colors, children's book style"
    
    print("\n🎨 Gerando imagem de teste...")
    image = generator.generate_image(
        test_prompt,
        width=512,
        height=512,
        num_inference_steps=20  # Menos steps para teste rápido
    )
    
    # Salvar
    os.makedirs("output/test", exist_ok=True)
    test_path = "output/test/stable_diffusion_test.png"
    image.save(test_path)
    
    print(f"\n✅ Imagem de teste salva em: {test_path}")
    print("   Abra para ver o resultado!")
    print("\n💡 Se a qualidade estiver boa, podemos gerar todas as imagens do e-book!")


if __name__ == "__main__":
    test_generator()
