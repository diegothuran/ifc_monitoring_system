# 🚀 Deploy no Heroku - IFC Monitoring System

## Pré-requisitos

1. **Conta no Heroku**: Crie uma conta em [heroku.com](https://heroku.com)
2. **Heroku CLI**: Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Certifique-se de que o Git está configurado

## Método 1: Deploy Automático (Recomendado)

### 1. Execute o script de deploy
```bash
python deploy_heroku.py
```

O script irá:
- Verificar se o Heroku CLI está instalado
- Verificar se você está logado
- Criar o app (se necessário)
- Configurar todas as variáveis de ambiente
- Adicionar o PostgreSQL
- Fazer o deploy
- Abrir o app no navegador

## Método 2: Deploy Manual

### 1. Login no Heroku
```bash
heroku login
```

### 2. Criar o app
```bash
heroku create nome-do-seu-app
```

### 3. Configurar variáveis de ambiente
```bash
# Gerar uma chave secreta segura
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" -a nome-do-seu-app

# Configurar outras variáveis
heroku config:set DEBUG=False -a nome-do-seu-app
heroku config:set LOG_LEVEL=INFO -a nome-do-seu-app
heroku config:set API_V1_STR="/api/v1" -a nome-do-seu-app
heroku config:set PROJECT_NAME="IFC Monitoring System" -a nome-do-seu-app
```

### 4. Adicionar PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini -a nome-do-seu-app
```

### 5. Fazer deploy
```bash
git push heroku main
```

### 6. Abrir o app
```bash
heroku open -a nome-do-seu-app
```

## Método 3: Deploy via Botão (Mais Fácil)

1. Faça um fork deste repositório
2. Clique no botão abaixo:
   [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/seu-usuario/ifc-monitoring-system)
3. Preencha o nome do app
4. Clique em "Deploy app"

## Verificação do Deploy

Após o deploy, verifique se tudo está funcionando:

1. **Página inicial**: `https://seu-app.herokuapp.com`
2. **Documentação da API**: `https://seu-app.herokuapp.com/docs`
3. **Health check**: `https://seu-app.herokuapp.com/health`

## Comandos Úteis

```bash
# Ver logs em tempo real
heroku logs --tail -a nome-do-seu-app

# Acessar o console do Heroku
heroku run python -a nome-do-seu-app

# Ver variáveis de ambiente
heroku config -a nome-do-seu-app

# Reiniciar o app
heroku restart -a nome-do-seu-app

# Ver informações do app
heroku apps:info -a nome-do-seu-app
```

## Troubleshooting

### Erro de Build
- Verifique se todas as dependências estão no `requirements.txt`
- Certifique-se de que o `Procfile` está correto

### Erro de Database
- Verifique se o PostgreSQL foi adicionado
- Confirme se a variável `DATABASE_URL` está configurada

### Erro de Porta
- Certifique-se de que o `Procfile` usa `$PORT`
- Verifique se o `main.py` está configurado corretamente

### Erro de CORS
- Verifique as configurações de CORS no `main.py`
- Confirme se o frontend está apontando para a URL correta

## Configuração do Frontend

Após o deploy, atualize o frontend para apontar para a nova URL:

```typescript
// frontend/src/services/api.ts
const API_BASE_URL = 'https://seu-app.herokuapp.com/api/v1';
```

## Monitoramento

- Use `heroku logs --tail` para monitorar logs em tempo real
- Configure alertas no painel do Heroku
- Monitore o uso de recursos no dashboard

## Backup do Banco de Dados

```bash
# Fazer backup
heroku pg:backups:capture -a nome-do-seu-app

# Restaurar backup
heroku pg:backups:restore BACKUP_ID DATABASE_URL -a nome-do-seu-app
```

## Atualizações

Para atualizar o app:

```bash
git add .
git commit -m "Atualização"
git push heroku main
```

---

✅ **Deploy concluído com sucesso!** Seu sistema IFC Monitoring está agora rodando na nuvem!
