# 🚀 Deploy Rápido no Heroku

## ⚡ Deploy em 5 Minutos

### 1. Pré-requisitos
- Conta no [Heroku](https://heroku.com)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Git configurado

### 2. Deploy Automático
```bash
# Execute o script de deploy
python deploy_heroku.py
```

### 3. Deploy Manual (se preferir)
```bash
# Login
heroku login

# Criar app
heroku create meu-app-ifc

# Configurar variáveis
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" -a meu-app-ifc
heroku config:set DEBUG=False -a meu-app-ifc

# Adicionar banco
heroku addons:create heroku-postgresql:mini -a meu-app-ifc

# Deploy
git push heroku main
```

### 4. Testar
```bash
# Testar se funcionou
python test_deploy.py
```

### 5. Configurar Frontend
1. Edite `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://meu-app-ifc.herokuapp.com/api/v1';
```

2. Deploy do frontend no Netlify:
- Faça push para GitHub
- Conecte ao Netlify
- Configure `REACT_APP_API_URL=https://meu-app-ifc.herokuapp.com/api/v1`

## ✅ Pronto!

Seu sistema estará rodando em:
- **Backend**: https://meu-app-ifc.herokuapp.com
- **API Docs**: https://meu-app-ifc.herokuapp.com/docs
- **Frontend**: https://meu-frontend.netlify.app

## 🔧 Comandos Úteis

```bash
# Ver logs
heroku logs --tail -a meu-app-ifc

# Reiniciar
heroku restart -a meu-app-ifc

# Abrir app
heroku open -a meu-app-ifc
```

## 🆘 Problemas?

- **Erro de build**: Verifique `requirements.txt`
- **Erro de banco**: Confirme se PostgreSQL foi adicionado
- **Erro de porta**: Verifique `Procfile`
- **Erro de CORS**: Confirme configuração no `main.py`
