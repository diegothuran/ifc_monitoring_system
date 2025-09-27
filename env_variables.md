# Variáveis de Ambiente - IFC Monitoring System

## Configuração para Deploy no Heroku

### Variáveis Obrigatórias

```bash
# Database (Heroku Postgres)
DATABASE_URL=postgresql://username:password@hostname:port/database

# JWT Secret Key (GERE UMA CHAVE SEGURA!)
SECRET_KEY=sua-chave-secreta-super-segura-aqui

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=IFC Monitoring System

# Development/Production
DEBUG=False
LOG_LEVEL=INFO
```

### Variáveis Opcionais

```bash
# Sensor Configuration
SENSOR_UPDATE_INTERVAL=60
ALERT_THRESHOLD_TEMPERATURE=80.0
ALERT_THRESHOLD_HUMIDITY=90.0
ALERT_THRESHOLD_PRESSURE=1013.25

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
ALERT_EMAIL_RECIPIENTS=admin@exemplo.com,alerts@exemplo.com

# Heroku specific
PORT=8000
```

## Como Configurar no Heroku

1. Instale o Heroku CLI
2. Faça login: `heroku login`
3. Crie o app: `heroku create nome-do-seu-app`
4. Configure as variáveis:
   ```bash
   heroku config:set SECRET_KEY="sua-chave-secreta-super-segura"
   heroku config:set DEBUG=False
   heroku config:set LOG_LEVEL=INFO
   ```
5. Adicione o addon do PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
6. Faça o deploy: `git push heroku main`
