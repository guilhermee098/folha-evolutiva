# 🚀 Deploy Rápido no Render.com

## ✅ Pré-requisitos
- Conta no GitHub
- Conta no Render.com (gratuita)
- Projeto limpo (sem arquivos pessoais)

---

## 📋 Passo a Passo

### 1. **Inicialize Git (se ainda não fez)**

```bash
git init
git add .
git commit -m "Deploy inicial - Gerador de Folha de Evolução"
```

### 2. **Crie Repositório no GitHub**

1. Acesse: https://github.com/new
2. Nome: `folha-evolutiva`
3. Privado ou Público (sua escolha)
4. **NÃO** inicialize com README
5. Clique em **Create repository**

### 3. **Conecte ao GitHub**

```bash
# Substitua SEU-USUARIO pelo seu usuário do GitHub
git remote add origin https://github.com/SEU-USUARIO/folha-evolutiva.git
git branch -M main
git push -u origin main
```

### 4. **Deploy no Render.com**

1. **Acesse:** https://render.com
2. **Crie conta** (pode usar conta do GitHub)
3. **Clique em:** "New +" → "Web Service"
4. **Conecte repositório:**
   - Se não aparecer, clique em "Configure account"
   - Autorize o Render a acessar seus repositórios
   - Selecione `folha-evolutiva`
5. **Configure:**
   - **Name:** `folha-evolutiva` (ou qualquer nome)
   - **Region:** Oregon (US West) ou Frankfurt (mais próximo do Brasil)
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Plan:** `Free`
6. **Clique em:** "Create Web Service"

### 5. **Aguarde o Deploy** ⏳

- O Render vai fazer o build automaticamente
- Leva cerca de **2-5 minutos**
- Você pode acompanhar os logs em tempo real

### 6. **Acesse sua Aplicação!** 🎉

URL gerada: `https://folha-evolutiva-xxxx.onrender.com`

---

## ⚙️ Configurações Importantes

### **Variáveis de Ambiente (se necessário)**

No painel do Render:
1. Vá em "Environment"
2. Adicione variáveis se precisar

**Exemplo:**
```
PORT=8000
PYTHONUNBUFFERED=1
```

### **Atualizar Aplicação**

Após fazer mudanças:
```bash
git add .
git commit -m "Descrição da mudança"
git push
```

O Render faz **deploy automático**! 🚀

---

## 🔧 Solução de Problemas

### Build Falhou?

1. **Verifique os logs** no painel do Render
2. **Problemas comuns:**
   - `requirements.txt` não encontrado → Verifique se está na raiz
   - `Dockerfile` com erro → Teste localmente primeiro
   - Dependências faltando → Adicione em `requirements.txt`

### Aplicação não responde?

1. **Health Check:** Verifique se `/health` funciona
2. **Logs:** Clique em "Logs" no painel do Render
3. **Reinicie:** Clique em "Manual Deploy" → "Deploy latest commit"

### Timeout no deploy?

- **Free tier** tem limitações
- Pode demorar mais na primeira vez
- Se persistir, tente **Railway** ou **Fly.io**

---

## 📊 Limitações do Plano Gratuito

✅ **O que está incluído:**
- 750 horas/mês (suficiente para uso contínuo)
- SSL grátis
- Deploy automático
- 512MB RAM

⚠️ **Limitações:**
- Aplicação **hiberna** após 15 min sem uso
- Primeira requisição após hibernar é **lenta** (~30s)
- Upload limitado a ~100MB

💡 **Solução para hibernação:**
Use um serviço de "ping" para manter ativo:
- https://uptimerobot.com (grátis)
- Ping a cada 14 minutos

---

## 🎯 URLs Importantes

Depois do deploy, você terá:

- **Aplicação:** `https://seu-app.onrender.com`
- **Interface:** `https://seu-app.onrender.com/`
- **API Docs:** `https://seu-app.onrender.com/docs`
- **Health Check:** `https://seu-app.onrender.com/health`

---

## 🔐 Segurança (Opcional)

### Tornar repositório privado:

1. GitHub → Repositório → Settings
2. Scroll até "Danger Zone"
3. "Change visibility" → "Make private"

### Adicionar autenticação básica (se quiser):

Edite `api.py` e adicione middleware de autenticação.

---

## 💰 Upgrade para Plano Pago (Opcional)

Se precisar de mais recursos:

- **Starter:** $7/mês
  - Sem hibernação
  - 512MB RAM
  - Deploy prioritário

- **Standard:** $25/mês
  - 2GB RAM
  - Mais performance

---

## ✅ Checklist Final

Antes de fazer commit:

- [ ] Arquivos `.docx` removidos de `entrada/` e `saida/`
- [ ] `.gitkeep` criados nas pastas
- [ ] `.gitignore` configurado
- [ ] `requirements.txt` atualizado
- [ ] `Dockerfile` presente
- [ ] `render.yaml` presente
- [ ] Template em `template_saida/`
- [ ] Testado localmente

---

## 🎉 Pronto!

Sua aplicação estará disponível globalmente em poucos minutos!

**Próximos passos:**
1. Teste o upload de arquivos
2. Compartilhe a URL com quem precisar
3. Configure ping para evitar hibernação (opcional)

---

**Dúvidas? Confira os logs no painel do Render!**
