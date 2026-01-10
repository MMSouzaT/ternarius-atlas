# 🔐 Como Obter sua Chave de API do Google Gemini

## Passo a Passo

### 1. Acesse o Google AI Studio
Visite: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 2. Faça Login
- Use sua conta do Google
- Aceite os termos de uso se solicitado

### 3. Crie uma Nova API Key
- Clique em "Create API Key" ou "Criar chave de API"
- Selecione ou crie um projeto do Google Cloud
- A chave será gerada automaticamente

### 4. Copie a Chave
- Copie a chave de API gerada (começa com "AIza...")
- **⚠️ IMPORTANTE**: Guarde esta chave em segurança!

### 5. Configure no Projeto
```bash
# No diretório do projeto
cp .env.example .env

# Edite o arquivo .env
nano .env

# Cole sua chave substituindo 'your_api_key_here'
GEMINI_API_KEY=AIzaSy...sua_chave_aqui
```

## ✅ Verificação

Teste se a configuração está correta:

```bash
python test_basic.py
```

Se tudo estiver certo, você verá:
```
🎉 All tests passed!
```

## 🔒 Segurança

**NÃO FAÇA**:
- ❌ Commitar o arquivo `.env` no git
- ❌ Compartilhar sua chave publicamente
- ❌ Usar a chave em código público

**FAÇA**:
- ✅ Mantenha o `.env` apenas local
- ✅ Use `.gitignore` para excluir `.env`
- ✅ Gere novas chaves se a atual vazar

## 💰 Custos

- Google Gemini tem um **tier gratuito generoso**
- Ideal para desenvolvimento e testes
- Verifique os limites em: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)

## 🆘 Problemas Comuns

### "API key not valid"
- Verifique se copiou a chave completa
- Certifique-se de que a API está habilitada no Google Cloud Console

### "Quota exceeded"
- Você atingiu o limite gratuito
- Aguarde a renovação ou configure billing

### "Permission denied"
- Habilite a API do Gemini no Google Cloud Console
- Vá em APIs & Services > Library > Busque "Gemini"

## 📚 Recursos Adicionais

- [Documentação do Google AI](https://ai.google.dev/)
- [Guia de Início Rápido](https://ai.google.dev/tutorials/python_quickstart)
- [Preços e Limites](https://ai.google.dev/pricing)

---

**Após configurar, você está pronto para gerar seu primeiro e-book! 🎉**

Execute:
```bash
python main.py
```
