# 📋 API Gerador de Folha de Evolução Transdisciplinar

API REST desenvolvida em FastAPI para automatizar a conversão de **Folhas de Frequência** em **Folhas de Evolução** formatadas.

## 🚀 Funcionalidades

- ✅ Upload de arquivos `.docx` (Folha de Frequência)
- ✅ Processamento automático e extração de dados
- ✅ Geração de Folha de Evolução formatada (baseada em template)
- ✅ Download direto do arquivo processado
- ✅ Interface web intuitiva e moderna
- ✅ Validação de arquivos e tratamento de erros
- ✅ Logging detalhado de operações

## 📦 Instalação

### 1. Clone o repositório (ou navegue até a pasta do projeto)

```bash
cd folha-evolutiva
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

### Opção 1: Executar diretamente

```bash
python api.py
```

### Opção 2: Executar com Uvicorn

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

## 🌐 Endpoints da API

### 1. **GET /** - Informações da API
Retorna informações gerais sobre a API.

**Resposta:**
```json
{
  "message": "API Gerador de Folha de Evolução Transdisciplinar",
  "version": "1.0.0",
  "endpoints": {
    "POST /processar": "Upload de arquivo de frequência e geração de evolução",
    "GET /health": "Status da API",
    "GET /config": "Configurações atuais"
  }
}
```

### 2. **GET /health** - Status da API
Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "ok",
  "message": "API está funcionando corretamente"
}
```

### 3. **GET /config** - Configurações Atuais
Retorna as configurações carregadas.

**Resposta:**
```json
{
  "config": {
    "duracao_atendimento_minutos": 40,
    "colunas_esperadas": ["DATA", "HORÁRIO", "PROCEDIMENTO"],
    "formato_hora": "%H:%M",
    "permitir_data_vazia_primeira_linha": true,
    "caminho_template": "template_saida/template_saida.docx",
    "extrair_cabecalho_de_entrada": true
  },
  "template_path": "template_saida/template_saida.docx",
  "template_exists": true
}
```

### 4. **POST /processar** - Processar Folha de Frequência
Envia um arquivo `.docx` e recebe a Folha de Evolução gerada.

**Parâmetros:**
- `arquivo` (FormData): Arquivo `.docx` da Folha de Frequência

**Resposta:**
- Arquivo `.docx` da Folha de Evolução (download direto)

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/processar" \
  -F "arquivo=@entrada/JOAO PAULO NUNES - Folha de frequência JULHO.docx" \
  --output "saida/Evolucao_JULHO.docx"
```

**Exemplo com Python:**
```python
import requests

url = "http://localhost:8000/processar"
files = {"arquivo": open("entrada/arquivo.docx", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("saida/evolucao.docx", "wb") as f:
        f.write(response.content)
    print("✓ Documento gerado com sucesso!")
else:
    print(f"✗ Erro: {response.json()['detail']}")
```

## 🖥️ Interface Web

Para facilitar o uso, foi criada uma interface web moderna e intuitiva.

### Como usar:

1. **Inicie a API:**
   ```bash
   python api.py
   ```

2. **Abra o arquivo `interface.html` no navegador:**
   - Clique duas vezes no arquivo `interface.html`, ou
   - Abra manualmente no navegador (Chrome, Firefox, Edge, etc.)

3. **Faça o upload:**
   - Clique na área de upload ou arraste o arquivo `.docx`
   - Clique em "Processar e Gerar Evolução"
   - O download será iniciado automaticamente

### Features da Interface:

- 🎨 Design moderno e responsivo
- 📤 Upload por clique ou drag-and-drop
- ⚡ Feedback visual em tempo real
- 📥 Download automático do resultado
- ✅ Validação de arquivos
- 🔄 Botão para enviar novo arquivo

## 📚 Documentação Interativa

A API possui documentação interativa automática gerada pelo FastAPI:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Nessas interfaces você pode:
- Ver todos os endpoints disponíveis
- Testar a API diretamente no navegador
- Ver exemplos de requisições e respostas
- Entender os parâmetros de cada endpoint

## 🔧 Configuração

A API utiliza o arquivo `config.json` (ou configurações padrão) para definir:

- Duração padrão dos atendimentos (minutos)
- Colunas esperadas na tabela de frequência
- Formato de hora
- Caminho do template de saída
- Opções de extração de cabeçalho

Para criar um arquivo de configuração personalizado, execute:

```bash
python main.py --gerar-config
```

## 📁 Estrutura do Projeto

```
folha-evolutiva/
├── api.py                    # API FastAPI
├── main.py                   # Lógica principal de processamento
├── interface.html            # Interface web
├── requirements.txt          # Dependências Python
├── config.json              # Configurações (opcional)
├── entrada/                 # Arquivos de entrada
├── saida/                   # Arquivos gerados
├── template_saida/          # Template da folha de evolução
│   └── template_saida.docx
├── temp_uploads/            # Uploads temporários (criado automaticamente)
└── temp_outputs/            # Outputs temporários (criado automaticamente)
```

## 🛡️ Tratamento de Erros

A API possui tratamento robusto de erros:

### Erro 400 - Bad Request
- Arquivo não é `.docx`
- Arquivo inválido ou corrompido
- Dados não encontrados no arquivo

### Erro 500 - Internal Server Error
- Template não encontrado
- Erro ao processar o documento
- Erro ao gerar o arquivo de saída

**Exemplo de resposta de erro:**
```json
{
  "detail": "Arquivo deve ser no formato .docx"
}
```

## 🧪 Testando a API

### Teste 1: Health Check
```bash
curl http://localhost:8000/health
```

### Teste 2: Obter Configurações
```bash
curl http://localhost:8000/config
```

### Teste 3: Processar Arquivo
```bash
curl -X POST "http://localhost:8000/processar" \
  -F "arquivo=@entrada/seu_arquivo.docx" \
  --output "saida/resultado.docx"
```

## 🚀 Deploy em Produção

### Deploy local com Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Deploy com Docker (exemplo):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy em Cloud:

A API pode ser facilmente deployada em:
- **Heroku**
- **AWS Lambda** (com Mangum)
- **Google Cloud Run**
- **Azure App Service**
- **Railway**
- **Render**

## 📊 Performance

- ⚡ Processamento médio: **1-3 segundos** por documento
- 💾 Memória: **~50MB** em repouso
- 🔄 Concorrência: Suporta múltiplas requisições simultâneas
- 📦 Arquivos temporários são automaticamente removidos

## 🔐 Segurança

- ✅ Validação de tipo de arquivo
- ✅ Validação de conteúdo do documento
- ✅ Arquivos temporários são removidos após processamento
- ✅ CORS configurado (ajuste para produção)
- ⚠️ **Importante:** Em produção, configure CORS adequadamente e adicione autenticação se necessário

## 📝 Logs

A API gera logs detalhados de todas as operações:

```
19:40:52 - INFO - → Recebendo arquivo: exemplo.docx
19:40:52 - INFO - ✓ Arquivo salvo temporariamente
19:40:52 - INFO - ✓ Arquivo válido e acessível
19:40:52 - INFO - ✓ Dados extraídos do cabeçalho
19:40:52 - INFO - ✓ Documento gerado com sucesso
```

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é de uso pessoal.

---

**Desenvolvido com ❤️ usando FastAPI e Python-docx**
