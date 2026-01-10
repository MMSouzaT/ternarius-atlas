# 🌟 Ternarius Atlas - Gerador de E-books com IA

Um projeto Python que gera E-books completos a partir de um tema fornecido pelo usuário, utilizando IA (Google Gemini) para gerar textos e imagens, mesclando-os em páginas individuais.

## 📋 Funcionalidades

- ✨ **Geração Automática de Conteúdo**: Cria títulos, capítulos e textos usando Google Gemini
- 🎨 **Ilustrações por IA**: Gera imagens ilustrativas para cada capítulo (placeholders visuais)
- 📄 **Páginas Completas**: Combina texto e imagens em páginas prontas para visualização
- 🎯 **Customizável**: Configure número de capítulos, páginas e inclusão de imagens
- 💾 **Saída em Imagens**: Cada página é salva como uma imagem PNG individual

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/MMSouzaT/ternarius-atlas.git
cd ternarius-atlas
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure a API do Google Gemini

1. Obtenha sua chave de API do Google Gemini em: https://makersuite.google.com/app/apikey
2. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
3. Edite o arquivo `.env` e adicione sua chave:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

## 📖 Uso

### Modo Interativo

Execute o script principal e siga as instruções:

```bash
python main.py
```

O programa irá perguntar:
- Tema do e-book
- Número de capítulos (padrão: 3)
- Páginas por capítulo (padrão: 2)
- Se deseja incluir imagens ilustrativas

### Modo Linha de Comando

Você também pode passar o tema diretamente:

```bash
python main.py "Inteligência Artificial"
```

### Uso Programático

```python
from ternarius_atlas import EbookGenerator

# Criar o gerador
generator = EbookGenerator(output_dir="output")

# Gerar e-book rápido (demo)
pages = generator.generate_quick_ebook(theme="Python para Iniciantes")

# Ou com configuração personalizada
pages = generator.generate_ebook(
    theme="História da Computação",
    num_chapters=5,
    pages_per_chapter=3,
    include_images=True,
    author="Seu Nome"
)
```

## 📁 Estrutura do Projeto

```
ternarius-atlas/
├── src/
│   └── ternarius_atlas/
│       ├── __init__.py           # Módulo principal
│       ├── config.py              # Configurações
│       ├── text_generator.py     # Geração de texto com Gemini
│       ├── image_generator.py    # Geração de imagens
│       ├── page_composer.py      # Composição de páginas
│       └── ebook_generator.py    # Orquestrador principal
├── examples/
│   └── example_usage.py          # Exemplos de uso
├── output/                        # Diretório de saída (gerado automaticamente)
├── main.py                        # Script principal
├── requirements.txt               # Dependências
├── .env.example                   # Exemplo de configuração
└── README.md                      # Este arquivo
```

## 🔧 Dependências

- **google-generativeai**: API do Google Gemini para geração de texto
- **Pillow**: Processamento de imagens
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **requests**: Requisições HTTP (futuras expansões)

## 📝 Exemplos

Veja exemplos completos de uso em `examples/example_usage.py`:

```bash
python examples/example_usage.py
```

## 🎨 Formato de Saída

O e-book gerado consiste em múltiplas imagens PNG:
- `page_000_cover.png` - Capa do e-book
- `page_001_title.png` - Página de título
- `page_002_ch1_p1.png` - Capítulo 1, Página 1
- `page_003_ch1_p2.png` - Capítulo 1, Página 2
- ... e assim por diante

Cada página tem:
- 800x1200 pixels (padrão, configurável)
- Texto formatado e ajustado automaticamente
- Imagens ilustrativas (opcional)
- Número de página
- Borda decorativa

## ⚙️ Configuração Avançada

Você pode personalizar as configurações editando `src/ternarius_atlas/config.py`:

```python
DEFAULT_PAGE_WIDTH = 800
DEFAULT_PAGE_HEIGHT = 1200
DEFAULT_FONT_SIZE = 24
DEFAULT_PADDING = 50
# ... e muito mais
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📄 Licença

Este projeto está sob desenvolvimento. Consulte o arquivo LICENSE para mais detalhes.

## 🙏 Agradecimentos

- Google Gemini pela API de IA
- Comunidade Python pelos pacotes incríveis

## 📞 Suporte

Se encontrar problemas:
1. Verifique se a chave da API está configurada corretamente
2. Certifique-se de que todas as dependências estão instaladas
3. Abra uma issue no GitHub com detalhes do erro

---

**Desenvolvido com ❤️ usando Python e Google Gemini**
