# 🎨 Ternarius Atlas - Gerador de E-books com IA

Gerador de e-books ilustrados usando Inteligência Artificial com suporte a **Stable Diffusion local** para imagens de alta qualidade.

## 🚀 Recursos

- ✅ Geração de texto com Google Gemini
- ✅ Geração de imagens com **Stable Diffusion** (local, GPU-accelerated)
- ✅ Sistema interativo em 3 etapas
- ✅ Criação de e-books para crianças
- ✅ Tons pastéis e personagens consistentes
- ✅ Organização automática em pastas

## 💻 Requisitos

### Para Usar Localmente (Recomendado - Rápido com GPU)

**Windows com RTX 3050:**
- Python 3.10 ou 3.11
- GPU NVIDIA RTX 3050 (8GB VRAM)
- 10-20 GB de espaço em disco
- Drivers NVIDIA atualizados

**Benchmark com RTX 3050:**
- Geração de imagem: 5-15 segundos ⚡
- E-book completo (8 páginas): ~2-3 minutos

## 🔧 Instalação Rápida (Windows)

```bash
# 1. Clone o repositório
git clone https://github.com/MMSouzaT/ternarius-atlas.git
cd ternarius-atlas

# 2. Execute o instalador automático
setup_windows.bat

# 3. Ative o ambiente (sempre que abrir novo terminal)
venv\Scripts\activate

# 4. Configure sua API key do Gemini
# Copie o arquivo .env.example para .env e adicione sua chave:
# GEMINI_API_KEY=sua_chave_aqui
```

**📖 Guia completo:** [SETUP_LOCAL_WINDOWS.md](SETUP_LOCAL_WINDOWS.md)

## 📚 Como Usar

### Modo 1: Sistema Interativo (3 Etapas)

```bash
python main.py
```

1. **Etapa 1:** Gerar estrutura do livro (você revisa e aprova)
2. **Etapa 2:** Gerar imagens com Stable Diffusion (você pode alterar)
3. **Etapa 3:** Adicionar textos às imagens (resultado final)

### Modo 2: Apenas Gerar Imagens com Stable Diffusion

```bash
python generate_images_sd.py
```

Gera imagens de alta qualidade usando sua GPU local.

## 🎯 Exemplo de E-book Criado

**"As Maravilhosas Histórias de Gênesis"**
- 8 páginas ilustradas
- Tons pastéis suaves
- Personagens consistentes (Adão, Eva, Noé)
- Textos para crianças até 10 anos
- [Ver estrutura](output/as_maravilhosas_historias_de_genesis/structure.json)

## ⚙️ Configurações

### Otimizado para RTX 3050 (8GB VRAM)

O sistema já vem configurado, mas você pode ajustar em `generate_images_sd.py`:

```python
CONFIG = {
    "model": "runwayml/stable-diffusion-v1-5",  # Rápido e eficiente
    "num_inference_steps": 30,  # 30=rápido, 50=mais qualidade
    "width": 800,
    "height": 1200,
}
```

### Modelos Disponíveis

| Modelo | VRAM | Velocidade RTX 3050 | Qualidade |
|--------|------|---------------------|-----------|
| SD 1.5 | ~4GB | 5-10 seg/img | Boa |
| SDXL | ~6-8GB | 15-25 seg/img | Excelente |

## 📂 Estrutura do Projeto

```
ternarius-atlas/
├── main.py                      # Sistema interativo
├── generate_images_sd.py        # Gerador com Stable Diffusion
├── setup_windows.bat            # Instalador automático
├── SETUP_LOCAL_WINDOWS.md       # Guia de instalação
├── requirements.txt             # Dependências
├── .env                         # API keys (criar)
├── src/
│   └── ternarius_atlas/
│       ├── text_generator.py    # Geração de texto
│       ├── image_generator.py   # Geração de imagens
│       ├── page_composer.py     # Composição de páginas
│       └── config.py            # Configurações
└── output/                      # E-books gerados
    └── [nome-do-livro]/
        ├── structure.json       # Estrutura
        ├── page_*_sd.png        # Imagens SD
        └── page_*_final.png     # Páginas finais
```

## 🐛 Solução de Problemas

### Verificar se GPU está funcionando
```bash
python test_gpu.py
```

### Erro: "CUDA out of memory"
- Feche outros programas que usam GPU
- Reduza `num_inference_steps` para 20
- Use modelo SD 1.5 (mais leve)

### Reinstalar PyTorch com CUDA
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## 📊 Performance Esperada

### RTX 3050 (8GB VRAM)
- **Imagem 800x1200:** 8-12 segundos
- **E-book 8 páginas:** ~2-3 minutos
- **Primeira execução:** +3-5 min (download do modelo 4GB)

### CPU (sem GPU)
- ⚠️ **Não recomendado:** 2-5 minutos por imagem

## 💡 Dicas

- **Primeira vez:** Aguarde o download do modelo (~4GB)
- **Modelos salvos em:** `C:\Users\VOCÊ\.cache\huggingface\`
- **Quer mais qualidade?** Aumente `num_inference_steps` para 50
- **Quer mais velocidade?** Use `num_inference_steps: 20`

## 🎓 Recursos

- [Documentação Stable Diffusion](https://stable-diffusion-art.com/)
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers)
- [Modelos Text-to-Image](https://huggingface.co/models?pipeline_tag=text-to-image)

## 📝 Licença

MIT License

## ✨ Próximas Features

- [ ] Interface web com Gradio
- [ ] Exportação para PDF/EPUB
- [ ] LoRAs customizados
- [ ] Mais modelos especializados
- [ ] Editor visual de páginas

---

**Feito com ❤️ e IA**

**Sua RTX 3050 está pronta para criar livros incríveis! 🚀📚**
