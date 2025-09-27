# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.1.0] - 2024-12-19

### 🚀 Adicionado
- **Deploy automatizado no Heroku** com script `deploy_heroku.py`
- **Configuração completa para Heroku** (Procfile, runtime.txt, app.json)
- **Scripts de configuração** (`setup_database.py`, `test_deploy.py`)
- **Documentação completa de deploy** (DEPLOY_HEROKU.md, QUICK_DEPLOY.md)
- **Suporte a PostgreSQL** para produção
- **Configuração de CORS** para deploy em produção
- **Variáveis de ambiente** para diferentes ambientes
- **Monitoramento e logs** configurados para produção

### 🔧 Modificado
- **README.md** completamente atualizado com:
  - Badges de status
  - Instruções de deploy em português
  - Seções reorganizadas com emojis
  - Guias passo-a-passo
  - Documentação de funcionalidades
- **main.py** atualizado para suportar porta do Heroku
- **backend/core/config.py** configurado para produção
- **requirements.txt** adicionado gunicorn
- **CORS** configurado para produção

### 📚 Documentação
- **DEPLOY_HEROKU.md** - Guia completo de deploy
- **QUICK_DEPLOY.md** - Deploy rápido em 5 minutos
- **env_variables.md** - Documentação das variáveis de ambiente
- **frontend_config_heroku.md** - Configuração do frontend
- **HEROKU_DEPLOY_SUMMARY.md** - Resumo do deploy

### 🛠️ Arquivos Criados
- `Procfile` - Configuração do Heroku
- `runtime.txt` - Versão do Python
- `app.json` - Configuração para deploy via botão
- `deploy_heroku.py` - Script de deploy automático
- `setup_database.py` - Configuração do banco
- `test_deploy.py` - Teste do deploy
- `.gitignore` - Arquivos ignorados pelo Git

## [1.0.0] - 2024-12-18

### 🎉 Lançamento Inicial
- Sistema completo de monitoramento IFC
- Backend FastAPI com SQLAlchemy
- Frontend React com Material-UI
- Autenticação JWT
- Gerenciamento de sensores e alertas
- Processamento de arquivos IFC
- Dashboard interativo
- API RESTful completa

---

## 🔄 Tipos de Mudanças

- **🚀 Adicionado** - Para novas funcionalidades
- **🔧 Modificado** - Para mudanças em funcionalidades existentes
- **🗑️ Removido** - Para funcionalidades removidas
- **🐛 Corrigido** - Para correções de bugs
- **📚 Documentação** - Para mudanças na documentação
- **🛠️ Arquivos** - Para novos arquivos criados
