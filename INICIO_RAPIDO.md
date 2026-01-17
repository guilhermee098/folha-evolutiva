# 🚀 INÍCIO RÁPIDO

## ⚡ Como Usar (Modo Mais Simples)

### 1. Inicie a API
```bash
python api.py
```

### 2. Acesse no Navegador
```
http://localhost:8000
```

### 3. Pronto!
- Arraste o arquivo .docx
- Clique em "Processar e Gerar Evolução"
- Download automático!

---

## ✅ Vantagens Desta Abordagem

- ✅ **Sem problemas de CORS** (navegador e API no mesmo domínio)
- ✅ **Sem necessidade de Live Server**
- ✅ **Um único comando** para rodar tudo
- ✅ **Mais simples e confiável**

---

## 🔧 Comandos Úteis

### Iniciar API
```bash
python api.py
```

### Testar via cURL
```bash
curl -X POST "http://localhost:8000/processar" \
  -F "arquivo=@entrada/arquivo.docx" \
  --output "saida/resultado.docx"
```

### Usar via CLI (sem API)
```bash
python main.py "entrada/arquivo.docx" "saida/resultado.docx"
```

---

## 📚 Documentação

- **Interface Web**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Configurações**: http://localhost:8000/config

---

## 🐛 Solução de Problemas

### Problema: "Failed to fetch"
**Solução:** 
1. Feche o Live Server (porta 5500)
2. Acesse **http://localhost:8000** (não 127.0.0.1:5500)
3. A API serve a interface diretamente, sem CORS

### Problema: Porta 8000 em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Problema: Arquivo não processa
1. Pressione **F12** no navegador
2. Vá na aba **Console**
3. Tente fazer upload novamente
4. Veja os logs detalhados

---

## 📁 Estrutura de Arquivos

```
folha-evolutiva/
├── api.py                  ← Servidor FastAPI
├── main.py                 ← Script CLI
├── interface.html          ← Interface web
├── requirements.txt        ← Dependências
├── entrada/                ← Coloque arquivos aqui
├── saida/                  ← Documentos gerados
└── template_saida/         ← Template de formatação
```

---

## 🎯 Modo de Uso Recomendado

**OPÇÃO 1: Interface Web (Recomendado)**
```bash
# 1. Inicie a API
python api.py

# 2. Acesse no navegador
# http://localhost:8000

# 3. Arraste o arquivo e clique em "Processar"
```

**OPÇÃO 2: Linha de Comando**
```bash
python main.py "entrada/arquivo.docx" "saida/resultado.docx"
```

**OPÇÃO 3: API REST (Para integração)**
```python
import requests

files = {"arquivo": open("entrada/arquivo.docx", "rb")}
response = requests.post("http://localhost:8000/processar", files=files)

with open("saida/evolucao.docx", "wb") as f:
    f.write(response.content)
```

---

**Desenvolvido com ❤️ usando Python, FastAPI e python-docx**
