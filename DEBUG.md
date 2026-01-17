# 🔍 Guia de Debug - Folha de Evolução

## ✅ Problemas Resolvidos

### 1. "Failed to fetch" no Frontend

**Sintoma:** Backend processa arquivo com sucesso (Status 200) mas frontend recebe erro "Failed to fetch".

**Causa:** 
- `FileResponse` com `background` task limpava arquivos antes da resposta ser completamente enviada
- Headers CORS não estavam sendo expostos corretamente

**Solução Implementada:**
1. ✅ Arquivo lido em memória ANTES de enviar
2. ✅ Limpeza de temporários ANTES da resposta
3. ✅ `Response` com bytes ao invés de `FileResponse`
4. ✅ Headers CORS explícitos
5. ✅ Timeout aumentado no frontend (60s)

---

## Melhorias Implementadas

### ✅ Logs detalhados no console do navegador (F12)
- Todos os passos do upload são logados
- Erros são capturados e exibidos com detalhes
- Stack trace completo disponível

### ✅ Middleware de logging na API
- Todas as requisições são logadas
- Tempo de processamento é registrado
- Erros são capturados globalmente

### ✅ Handler global de exceções
- Qualquer erro não tratado é capturado
- Logs detalhados com traceback completo

---

## 🧪 Como Testar e Identificar o Problema:

### Passo 1: Abra o Console do Navegador
1. Abra `interface.html` no navegador
2. Pressione **F12** para abrir o Developer Tools
3. Vá na aba **Console**

### Passo 2: Tente Fazer Upload de Outro Arquivo
1. Arraste ou selecione o arquivo problemático
2. Clique em "Processar"
3. **Observe os logs no console**

Você verá logs como:
```
=== INICIANDO PROCESSAMENTO ===
Arquivo: nome_do_arquivo.docx
Tamanho: 123456 bytes
Tipo: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Enviando requisição para: http://localhost:8000/processar
Status da resposta: 400 (ou outro código)
```

### Passo 3: Verifique os Logs do Servidor
Abra o terminal onde a API está rodando e procure por:
```
============================================================
NOVA REQUISICAO - Arquivo: nome_do_arquivo.docx
============================================================
```

---

## 🔍 Possíveis Causas do Problema:

### 1. **Arquivo não é .docx válido**
**Sintoma:** Erro 400 - "Arquivo inválido ou corrompido"

**Verificar:**
- O arquivo abre no Word/LibreOffice?
- É realmente um .docx ou é .doc (formato antigo)?

**Solução:** Abra no Word e salve como .docx novamente

---

### 2. **Estrutura de tabelas diferente**
**Sintoma:** Erro 400 - "Nenhum dado válido encontrado"

**Verificar:**
- O arquivo tem tabelas com as colunas: DATA, HORÁRIO, PROCEDIMENTO?
- Os nomes das colunas estão exatamente assim (com acento)?

**Logs no servidor:**
```
Identificando e extraindo tabelas...
Nenhum dado valido encontrado no arquivo
```

**Solução:** Verifique se as tabelas seguem o padrão esperado

---

### 3. **Cabeçalho diferente**
**Sintoma:** Documento gerado mas com dados incorretos no cabeçalho

**Verificar:**
- O cabeçalho tem as informações: Nome, Nasc., Diagnóstico?
- Os textos estão no formato esperado?

**Logs no servidor:**
```
Extraindo dados do cabecalho...
Nenhum dado de cabecalho extraido
```

**Solução:** Ajuste o cabeçalho para seguir o padrão ou desative extração de cabeçalho

---

### 4. **Especialidades não reconhecidas**
**Sintoma:** Documento gerado mas sem tabelas ou com tabelas vazias

**Verificar:**
- As especialidades estão escritas corretamente na coluna PROCEDIMENTO?
- Exemplos esperados: FISIOTERAPIA, FONOAUDIOLOGIA, PSICOLOGIA, PSICOPEDAGOGIA, TERAPIA OCUPACIONAL

**Logs no servidor:**
```
Dados extraidos com sucesso:
  - Total de registros: 0
  - Especialidades encontradas: 0
```

**Solução:** Certifique-se de que os nomes das especialidades estão corretos

---

## 🛠️ Comandos Úteis de Debug:

### Testar arquivo via linha de comando:
```bash
python main.py "entrada/seu_arquivo.docx" "saida/teste.docx"
```
Isso mostrará logs detalhados no terminal.

### Testar arquivo via cURL:
```bash
curl -X POST "http://localhost:8000/processar" \
  -F "arquivo=@entrada/seu_arquivo.docx" \
  --output "saida/teste.docx" -v
```

### Ver logs em tempo real da API:
Os logs aparecem automaticamente no terminal onde você executou `python api.py`

---

## 📋 Checklist para Arquivo de Entrada Válido:

- [ ] Arquivo é .docx (não .doc)
- [ ] Arquivo abre no Word sem erros
- [ ] Tem pelo menos uma tabela
- [ ] Tabela tem colunas: DATA, HORÁRIO, PROCEDIMENTO (exatamente assim)
- [ ] Coluna PROCEDIMENTO tem especialidades válidas
- [ ] Cabeçalho tem informações do paciente (opcional)
- [ ] Arquivo não está corrompido

---

## 💡 Próximos Passos:

1. **Tente fazer upload do arquivo problemático**
2. **Copie todos os logs do console (F12)**
3. **Copie os logs do servidor (terminal da API)**
4. **Compartilhe os logs para análise**

Com essas informações, poderemos identificar exatamente o que está causando o problema!

---

## 🚀 Arquivos Atualizados:

- ✅ `interface.html` - Logs detalhados no console do navegador
- ✅ `api.py` - Middleware de logging + handler global de exceções
- ✅ Logs capturados em TODAS as requisições
