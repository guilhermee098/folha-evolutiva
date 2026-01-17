# 📋 Gerador de Folha de Evolução Transdisciplinar

Sistema automatizado para conversão de **Folhas de Frequência** em **Folhas de Evolução** formatadas, com API REST e interface web.

## 🎯 Funcionalidades

- ✅ Extração automática de dados de documentos Word (.docx)
- ✅ Identificação inteligente de especialidades (Fisioterapia, Fonoaudiologia, Psicologia, etc.)
- ✅ Geração de documento formatado baseado em template
- ✅ Preservação completa de formatação (fontes, cores, margens, logo, cabeçalho)
- ✅ API REST para integração
- ✅ Interface web moderna e intuitiva
- ✅ Logs detalhados de processamento
- ✅ Validação e tratamento de erros

## 🚀 Início Rápido

### Modo Mais Simples (Recomendado)

```bash
# 1. Instale as dependências (apenas primeira vez)
pip install -r requirements.txt

# 2. Inicie a API
python api.py

# 3. Acesse no navegador
# http://localhost:8000

# 4. Arraste o arquivo .docx e clique em "Processar"
```

A API serve a interface web diretamente, eliminando problemas de CORS!

---

### Alternativa: Linha de Comando

```bash
python main.py "entrada/arquivo.docx" "saida/resultado.docx"
```

## 📁 Estrutura do Projeto

```
folha-evolutiva/
├── main.py                  # Script principal (CLI)
├── api.py                   # API FastAPI
├── interface.html           # Interface web
├── requirements.txt         # Dependências Python
├── API_README.md           # Documentação detalhada da API
├── testar_api.py           # Script de testes
├── entrada/                # Arquivos de entrada
├── saida/                  # Documentos gerados
└── template_saida/         # Template de formatação
    └── template_saida.docx
```

## 🌐 API REST

### Iniciar o Servidor

```bash
python api.py
```

Servidor disponível em: **http://localhost:8000**

### Endpoints Principais

- **GET /** - Informações da API
- **GET /health** - Status da API
- **GET /config** - Configurações atuais
- **POST /processar** - Processar folha de frequência
- **GET /docs** - Documentação interativa (Swagger UI)

### Exemplo de Uso com cURL

```bash
curl -X POST "http://localhost:8000/processar" \
  -F "arquivo=@entrada/arquivo.docx" \
  --output "saida/resultado.docx"
```

### Exemplo de Uso com Python

```python
import requests

files = {"arquivo": open("entrada/arquivo.docx", "rb")}
response = requests.post("http://localhost:8000/processar", files=files)

with open("saida/evolucao.docx", "wb") as f:
    f.write(response.content)
```

## 🖥️ Interface Web

A interface web oferece:

- 🎨 Design moderno e responsivo
- 📤 Upload por clique ou drag-and-drop
- ⚡ Feedback visual em tempo real
- 📥 Download automático do resultado
- ✅ Validação de arquivos
- 🔄 Suporte a múltiplos uploads

**Como usar:**

1. Inicie a API: `python api.py`
2. Abra `interface.html` no navegador
3. Arraste ou clique para selecionar o arquivo
4. Clique em "Processar e Gerar Evolução"
5. O download será iniciado automaticamente

## 📝 Logs Detalhados

A API gera logs completos de todas as operações:

```
============================================================
NOVA REQUISICAO - Arquivo: exemplo.docx
============================================================
Validacao: Formato .docx OK
Arquivo salvo: temp_uploads\tmp123.docx
Tamanho: 145234 bytes (0.14 MB)
Validacao: Arquivo integro OK
Carregando configuracoes...
Template encontrado: template_saida/template_saida.docx
Extraindo dados do cabecalho...
Cabecalho extraido: 5 campos
  - nome_paciente: João Paulo Braz Nunes
  - iniciais: JPBN
  - data_nascimento: 27/12/2018
  - mes_ano: JULHO/2025
  - cids: F84.9 Transtornos Globais...
Identificando e extraindo tabelas...
Dados extraidos com sucesso:
  - Total de registros: 54
  - Especialidades encontradas: 5
    * FISIOTERAPIA: 6 atendimento(s)
    * FONOAUDIOLOGIA: 5 atendimento(s)
    * PSICOLOGIA: 11 atendimento(s)
    * PSICOPEDAGOGIA: 16 atendimento(s)
    * TERAPIA OCUPACIONAL: 16 atendimento(s)
Gerando documento de evolucao...
Documento gerado com sucesso!
  - Tamanho: 68544 bytes (0.07 MB)
  - Registros processados: 54
  - Especialidades: 5
Enviando arquivo para o cliente...
```

## ⚙️ Configuração

O sistema pode ser configurado via arquivo `config.json` (opcional):

```json
{
  "duracao_atendimento_minutos": 40,
  "colunas_esperadas": ["DATA", "HORÁRIO", "PROCEDIMENTO"],
  "formato_hora": "%H:%M",
  "permitir_data_vazia_primeira_linha": true,
  "caminho_template": "template_saida/template_saida.docx",
  "extrair_cabecalho_de_entrada": true
}
```

Para gerar o arquivo de configuração:

```bash
python main.py --gerar-config
```

## 🔧 Requisitos

- Python 3.8+
- python-docx 1.1.2
- FastAPI 0.109.0
- Uvicorn 0.27.0
- lxml >= 5.1.0
- Pillow >= 10.2.0

## 📚 Documentação Adicional

- **API_README.md** - Documentação completa da API REST
- **http://localhost:8000/docs** - Documentação interativa (Swagger)
- **http://localhost:8000/redoc** - Documentação alternativa (ReDoc)

## 🧪 Testes

Execute o script de testes para verificar se tudo está funcionando:

```bash
python testar_api.py
```

## 🛡️ Tratamento de Erros

O sistema possui tratamento robusto de erros:

- ✅ Validação de formato de arquivo (.docx)
- ✅ Verificação de integridade do documento
- ✅ Validação de estrutura de tabelas
- ✅ Tratamento de dados faltantes
- ✅ Logs de erros detalhados
- ✅ Mensagens de erro claras

## 📊 Performance

- ⚡ Processamento: **1-3 segundos** por documento
- 💾 Memória: **~50MB** em repouso
- 🔄 Suporta múltiplas requisições simultâneas
- 📦 Limpeza automática de arquivos temporários

## 🎓 Uso Pessoal

Este projeto foi desenvolvido para uso pessoal e não possui licença específica.

---

**Desenvolvido com ❤️ usando Python, FastAPI e python-docx**
