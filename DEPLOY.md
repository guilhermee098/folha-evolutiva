# 🚀 Deploy na VPS com Docker

## Pré-requisitos
- VPS com Ubuntu/Debian
- Acesso SSH
- Domínio apontado para o IP da VPS (opcional)

## Passo 1: Preparar VPS

```bash
# Conectar via SSH
ssh seu_usuario@seu_ip

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout e login novamente
exit
ssh seu_usuario@seu_ip
```

## Passo 2: Upload do Projeto

```bash
# Opção 1: Git
cd /var/www
git clone seu-repositorio folha-evolutiva

# Opção 2: SCP (do seu PC)
scp -r folha-evolutiva/ seu_usuario@seu_ip:/var/www/
```

## Passo 3: Build e Deploy

```bash
cd /var/www/folha-evolutiva

# Build e inicie
docker-compose up -d --build

# Verifique logs
docker-compose logs -f

# Teste
curl http://localhost:8000/health
```

## Passo 4: Configurar Nginx (Opcional)

```bash
# Instalar Nginx
sudo apt install nginx -y

# Criar configuração
sudo nano /etc/nginx/sites-available/folha-evolutiva
```

**Conteúdo:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Ativar:**
```bash
sudo ln -s /etc/nginx/sites-available/folha-evolutiva /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Passo 5: SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

## Comandos Úteis

```bash
# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f folha-evolutiva

# Restart
docker-compose restart

# Parar
docker-compose down

# Rebuild após mudanças
docker-compose up -d --build

# Atualizar código
cd /var/www/folha-evolutiva
git pull
docker-compose up -d --build
```

## Segurança

```bash
# Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Auto-updates (opcional)
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## Backup Automático

```bash
# Criar script de backup
nano ~/backup.sh
```

**Conteúdo:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/folha-evolutiva"
mkdir -p $BACKUP_DIR

# Backup arquivos
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz \
  /var/www/folha-evolutiva/entrada \
  /var/www/folha-evolutiva/saida \
  /var/www/folha-evolutiva/template_saida

# Manter apenas últimos 7 dias
find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +7 -delete
```

**Agendar:**
```bash
chmod +x ~/backup.sh
crontab -e
# Adicione: 0 2 * * * /home/seu_usuario/backup.sh
```

## Monitoramento

```bash
# Ver uso de recursos
docker stats

# Ver logs em tempo real
docker-compose logs -f --tail=100
```

## Acesso

- **HTTP:** http://seu-dominio.com
- **HTTPS:** https://seu-dominio.com
- **API Docs:** https://seu-dominio.com/docs
- **Health:** https://seu-dominio.com/health

---

**Pronto! Sua aplicação está no ar! 🎉**
