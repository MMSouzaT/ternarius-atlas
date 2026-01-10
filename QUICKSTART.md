# 🎯 Guia Rápido de Início

## Configuração Inicial (5 minutos)

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key
```bash
# 1. Copie o arquivo de exemplo
cp .env.example .env

# 2. Obtenha sua chave em: https://makersuite.google.com/app/apikey

# 3. Edite o arquivo .env e cole sua chave
nano .env  # ou use seu editor favorito
```

### 3️⃣ Executar o Gerador

**Modo Interativo:**
```bash
python main.py
```

**Modo Linha de Comando:**
```bash
python main.py "Inteligência Artificial e o Futuro"
```

**Modo Programático:**
```python
from ternarius_atlas import EbookGenerator

generator = EbookGenerator()
pages = generator.generate_quick_ebook("Python para Iniciantes")
print(f"Gerado {len(pages)} páginas!")
```

## 📊 O Que Será Gerado

O programa criará múltiplos arquivos PNG no diretório `output/`:

```
output/
├── page_000_cover.png       # Capa colorida com título
├── page_001_title.png        # Página de título
├── page_002_ch1_p1.png       # Capítulo 1, Página 1 (com imagem)
├── page_003_ch1_p2.png       # Capítulo 1, Página 2
├── page_004_ch2_p1.png       # Capítulo 2, Página 1 (com imagem)
└── ...
```

## 🎨 Características das Páginas

- **Dimensões**: 800x1200 pixels (tamanho padrão de e-book)
- **Elementos**:
  - Capa colorida com gradiente
  - Título formatado e centralizado
  - Texto ajustado automaticamente
  - Imagens ilustrativas (opcional)
  - Número de página
  - Bordas decorativas

## ⚡ Exemplo Completo

```python
from ternarius_atlas import EbookGenerator

# Criar gerador
generator = EbookGenerator(output_dir="meu_ebook")

# Gerar e-book personalizado
pages = generator.generate_ebook(
    theme="História da Programação",
    num_chapters=4,          # 4 capítulos
    pages_per_chapter=3,     # 3 páginas cada
    include_images=True,     # Com ilustrações
    author="João Silva"      # Seu nome
)

print(f"✅ Sucesso! {len(pages)} páginas criadas em 'meu_ebook/'")

# Listar todas as páginas geradas
for page in pages:
    print(f"   📄 {page}")
```

## 🔧 Solução de Problemas

### Erro: "GEMINI_API_KEY não encontrada"
**Solução**: Verifique se o arquivo `.env` existe e contém sua chave da API.

### Erro: "No module named 'ternarius_atlas'"
**Solução**: Execute o script do diretório raiz do projeto ou ajuste o PYTHONPATH.

### Páginas vazias ou com erros
**Solução**: Verifique sua conexão com a internet e se a API key é válida.

## 📚 Recursos Adicionais

- **Exemplos**: Veja `examples/example_usage.py` para mais exemplos
- **Testes**: Execute `python test_basic.py` para verificar a instalação
- **Configuração**: Edite `src/ternarius_atlas/config.py` para personalizar

## 🎓 Próximos Passos

1. **Gere seu primeiro e-book**: Use um tema simples para testar
2. **Experimente configurações**: Mude número de capítulos e páginas
3. **Personalize**: Ajuste cores, tamanhos e estilos no código
4. **Compartilhe**: As páginas PNG podem ser convertidas em PDF ou outros formatos

## 💡 Dicas

- Use temas específicos para melhores resultados: "Machine Learning com Python" vs "Tecnologia"
- Para e-books longos, gere em partes (evita timeout da API)
- Combine páginas PNG em PDF usando ferramentas como `img2pdf` ou `PyPDF2`

---

**Pronto para começar? Execute `python main.py` agora! 🚀**
