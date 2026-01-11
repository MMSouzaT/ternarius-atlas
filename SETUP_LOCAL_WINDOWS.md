# 🚀 Setup para Windows com RTX 3050

## ✅ Seu Hardware
- **GPU:** NVIDIA GeForce RTX 3050 (8GB VRAM)
- **Sistema:** Windows
- **Velocidade esperada:** 5-15 segundos por imagem ⚡

---

## 📋 Pré-requisitos

### 1. Instalar Python 3.10 ou 3.11
- Download: https://www.python.org/downloads/
- **IMPORTANTE:** Marque "Add Python to PATH" durante instalação
- Recomendado: Python 3.10.11 ou 3.11.x

### 2. Instalar Git
- Download: https://git-scm.com/download/win
- Use configurações padrão

### 3. Verificar NVIDIA Drivers
- Drivers atualizados: https://www.nvidia.com/Download/index.aspx
- Mínimo: Driver 522.06 ou superior

---

## 🔧 Instalação Rápida

### Opção 1: Instalação Automática (Recomendado)

1. **Clone o repositório (se ainda não clonou):**
```bash
git clone https://github.com/SEU_USUARIO/ternarius-atlas.git
cd ternarius-atlas
```

2. **Execute o script de instalação:**
```bash
setup_windows.bat
```

Isso vai:
- Criar ambiente virtual Python
- Instalar PyTorch com suporte CUDA
- Instalar Stable Diffusion e dependências
- Baixar modelo otimizado (3-5 GB)
- Configurar tudo automaticamente

### Opção 2: Instalação Manual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate

# Instalar PyTorch com CUDA (para RTX 3050)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Instalar dependências
pip install diffusers transformers accelerate safetensors xformers

# Instalar outras dependências do projeto
pip install -r requirements.txt
```

---

## 🎨 Usar o Gerador de E-books

### 1. Ativar ambiente virtual (toda vez que abrir novo terminal)
```bash
venv\Scripts\activate
```

### 2. Gerar e-book completo
```bash
python main.py
```

### 3. Apenas gerar imagens com Stable Diffusion
```bash
python generate_images_sd.py
```

---

## ⚙️ Configurações Otimizadas para RTX 3050

O sistema já está pré-configurado para sua GPU, mas você pode ajustar em `config.py`:

```python
# Para RTX 3050 (8GB VRAM)
STABLE_DIFFUSION_CONFIG = {
    "model": "runwayml/stable-diffusion-v1-5",  # Modelo leve e rápido
    "enable_xformers": True,  # Otimização de memória
    "enable_attention_slicing": True,  # Economiza VRAM
    "num_inference_steps": 30,  # 30 = rápido, 50 = melhor qualidade
    "guidance_scale": 7.5,
    "width": 800,
    "height": 1200
}
```

### Se quiser mais qualidade (um pouco mais lento):
```python
"model": "stabilityai/stable-diffusion-xl-base-1.0"  # SDXL (mais pesado)
"num_inference_steps": 50
```

---

## 🐛 Solução de Problemas

### Erro: "CUDA out of memory"
- Feche outros programas que usam GPU
- Reduza resolução das imagens
- Ative `enable_attention_slicing`

### Erro: "torch not found" ou "CUDA not available"
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Verificar se GPU está sendo usada:
```bash
python test_gpu.py
```

### Imagens muito lentas
- Verifique se está usando a GPU (não CPU)
- Atualize drivers NVIDIA
- Feche navegador e outros programas pesados

---

## 📊 Benchmark Esperado (RTX 3050)

| Modelo | Resolução | Tempo/Imagem |
|--------|-----------|--------------|
| SD 1.5 | 512x512 | 3-5 seg |
| SD 1.5 | 800x1200 | 8-12 seg |
| SDXL | 800x1200 | 15-25 seg |

---

## 🎯 Próximos Passos

1. ✅ Instalar tudo (use `setup_windows.bat`)
2. ✅ Testar com `python test_gpu.py`
3. ✅ Gerar seu primeiro e-book com `python main.py`
4. ✅ Ajustar configurações se necessário

---

## 💡 Dicas

- **Primeira execução:** Pode demorar mais (baixa o modelo ~3-5GB)
- **Modelos ficam em:** `C:\Users\SEU_USUARIO\.cache\huggingface\`
- **Para e-books infantis:** SD 1.5 é perfeito e mais rápido que SDXL
- **Salve suas configurações favoritas** no arquivo `.env`

---

## 📞 Suporte

Se tiver problemas:
1. Verifique se Python está no PATH
2. Verifique se drivers NVIDIA estão atualizados
3. Execute `python test_gpu.py` para diagnóstico
4. Veja os logs de erro completos

**Tudo pronto! Sua RTX 3050 vai voar! 🚀**
