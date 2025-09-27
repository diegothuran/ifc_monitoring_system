# 🏭 IFC Monitoring System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![Heroku](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema completo de monitoramento de instalações industriais** com processamento de arquivos IFC, monitoramento de sensores em tempo real e alertas automatizados.

## 🎯 Visão Geral

O **IFC Monitoring System** é uma solução completa para monitoramento de instalações industriais, construída com **FastAPI** (backend) e **React** (frontend). O sistema oferece monitoramento em tempo real de sensores ambientais, alertas automatizados e capacidades abrangentes de gerenciamento para instalações industriais.

### 🌟 Principais Benefícios
- ✅ **Monitoramento em Tempo Real** - Acompanhe sensores 24/7
- ✅ **Alertas Inteligentes** - Notificações automáticas quando limites são excedidos
- ✅ **Processamento IFC** - Upload e análise de arquivos de construção
- ✅ **Interface Moderna** - Dashboard responsivo e intuitivo
- ✅ **Deploy Fácil** - Deploy automatizado no Heroku em minutos
- ✅ **API Completa** - Integração com sistemas externos

## 🚀 Quick Start

### Opção 1: Deploy Rápido no Heroku (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ifc-monitoring-system.git
cd ifc-monitoring-system

# Deploy automático
python deploy_heroku.py
```

### Opção 2: Execução Local
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar dependências do frontend
cd frontend && npm install && cd ..

# Iniciar o sistema completo
python start_system.py
```

### Opção 3: Deploy via Botão (Mais Fácil)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/seu-usuario/ifc-monitoring-system)

> **Nota**: O script `start_system.py` automaticamente:
> - Verifica dependências
> - Cria dados de exemplo se necessário
> - Inicia servidores backend e frontend
> - Abre o navegador na aplicação

## ✨ Funcionalidades

### 🎛️ Funcionalidades Principais
- **🔍 Monitoramento em Tempo Real**: Acompanhe temperatura, umidade, pressão e outros parâmetros ambientais
- **🚨 Sistema de Alertas Automatizado**: Alertas inteligentes quando leituras excedem limites configuráveis
- **🏢 Suporte Multi-localização**: Organize sensores por edifício, andar, sala e hierarquia de zonas
- **👥 Controle de Acesso Baseado em Funções**: Funções Admin, Operador e Visualizador com permissões apropriadas
- **📊 Dashboard Interativo**: Visão geral em tempo real do status do sistema e leituras de sensores
- **📁 Processamento de Arquivos IFC**: Upload e processamento de arquivos de construção IFC (Industry Foundation Classes)
- **🔗 API RESTful Completa**: API completa para integração com sistemas externos

### 🎨 Interface do Usuário
- **⚛️ Frontend React Moderno**: Construído com Material-UI para uma aparência profissional
- **📱 Design Responsivo**: Funciona em desktop, tablet e dispositivos móveis
- **🔄 Atualizações em Tempo Real**: Atualização de dados ao vivo e notificações
- **🎯 Gerenciamento Intuitivo**: Formulários fáceis de usar para sensores, localizações e alertas
- **📈 Gráficos Interativos**: Representação visual das tendências dos dados dos sensores

### 🚀 Deploy e Infraestrutura
- **☁️ Deploy Automático no Heroku**: Deploy em minutos com scripts automatizados
- **🐳 Suporte Docker**: Containerização completa para deploy em qualquer ambiente
- **🔧 Configuração Flexível**: Variáveis de ambiente para diferentes ambientes
- **📊 Monitoramento Integrado**: Logs e métricas para monitoramento de produção

## 🏗️ Arquitetura

### 🔧 Backend (FastAPI + SQLAlchemy)
- **⚡ FastAPI**: Framework web moderno e rápido para construção de APIs
- **🗄️ SQLAlchemy**: ORM poderoso para operações de banco de dados
- **🔐 Autenticação JWT**: Autenticação segura baseada em tokens
- **⚙️ Serviços em Background**: Monitoramento automatizado de sensores e processamento de alertas
- **📁 Processamento IFC**: Suporte integrado para análise de arquivos IFC
- **💾 Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)

### 🎨 Frontend (React + Material-UI)
- **⚛️ React 18**: React moderno com hooks e componentes funcionais
- **🎨 Material-UI**: Biblioteca de componentes profissional
- **🔄 React Query**: Busca e cache eficiente de dados
- **📝 TypeScript**: Desenvolvimento com tipagem segura
- **📱 Design Responsivo**: Abordagem mobile-first

### 🗃️ Modelos de Banco de Dados
- **👤 User**: Autenticação e autorização
- **📍 Location**: Gerenciamento hierárquico de localizações
- **📡 Sensor**: Configuração e metadados de sensores
- **📊 SensorReading**: Dados de séries temporais de sensores
- **🚨 Alert**: Gerenciamento e rastreamento de alertas
- **📁 IFCFile**: Metadados de arquivos IFC e status de processamento
- **🏢 IFCSpace**: Espaços de construção extraídos de arquivos IFC

### 🚀 Infraestrutura de Deploy
- **☁️ Heroku**: Deploy automatizado com PostgreSQL
- **🐳 Docker**: Containerização para deploy em qualquer ambiente
- **📊 Monitoramento**: Logs e métricas integradas
- **🔧 CI/CD**: Pipeline automatizado de deploy

## 📦 Instalação

### 📋 Pré-requisitos
- **Python 3.11+** (recomendado 3.11.6)
- **Node.js 16+** (recomendado 18+)
- **npm** ou **yarn**
- **Git** para clonagem do repositório

### 🛠️ Instalação Manual

1. **📥 Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/ifc-monitoring-system.git
cd ifc_monitoring_system
```

2. **🐍 Configure o ambiente Python:**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

3. **⚛️ Configure o frontend:**
```bash
cd frontend
npm install
cd ..
```

4. **📊 Criar dados de exemplo:**
```bash
python create_sample_data.py
```

5. **🚀 Iniciar o sistema:**
```bash
# Opção 1: Script automatizado (recomendado)
python start_system.py

# Opção 2: Manual (duas janelas de terminal)
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend && npm start
```

### 🐳 Instalação com Docker (Opcional)
```bash
# Build da imagem
docker build -t ifc-monitoring .

# Executar container
docker run -p 8000:8000 -p 3000:3000 ifc-monitoring
```

## ⚙️ Configuração

### 🔧 Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz:

```env
# 🗄️ Configuração do Banco de Dados
DATABASE_URL=sqlite:///./ifc_monitoring.db

# 🔐 Configuração JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 🔗 Configuração da API
API_V1_STR=/api/v1
PROJECT_NAME=IFC Monitoring System

# 📡 Configuração dos Sensores
SENSOR_UPDATE_INTERVAL=60
ALERT_THRESHOLD_TEMPERATURE=80.0
ALERT_THRESHOLD_HUMIDITY=90.0
ALERT_THRESHOLD_PRESSURE=1013.25

# 📧 Configuração de Email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_RECIPIENTS=admin@company.com,operator@company.com

# 🛠️ Desenvolvimento/Produção
DEBUG=True
LOG_LEVEL=INFO
```

### 🚀 Configuração para Deploy

Para deploy em produção, configure as seguintes variáveis:

```env
# Produção
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=chave-super-segura-para-producao

# Heroku (automático)
DATABASE_URL=postgresql://...  # Configurado automaticamente pelo Heroku
PORT=8000  # Configurado automaticamente pelo Heroku
```

## 🎯 Como Usar

### 🌐 Pontos de Acesso
- **🎨 Aplicação Frontend**: http://localhost:3000
- **🔗 API Backend**: http://localhost:8000
- **📚 Documentação da API**: http://localhost:8000/docs
- **🔄 API Interativa**: http://localhost:8000/redoc

### 👤 Credenciais de Login Padrão
O sistema cria usuários de exemplo automaticamente:

| Função | Usuário | Senha | Permissões |
|--------|---------|-------|------------|
| **Admin** | admin | admin123 | Acesso completo ao sistema |
| **Operador** | operator | operator123 | Gerenciar sensores e alertas |
| **Visualizador** | viewer | viewer123 | Acesso somente leitura |

### 🔑 Funcionalidades Principais

#### 📊 Dashboard
- Estatísticas do sistema em tempo real
- Visão geral de alertas recentes
- Últimas leituras de sensores
- Indicadores de saúde do sistema

#### 📡 Gerenciamento de Sensores
- Adicionar/editar/deletar sensores
- Configurar limites de alerta
- Atribuir sensores a localizações
- Monitorar status dos sensores

#### 🚨 Gerenciamento de Alertas
- Visualizar alertas ativos
- Reconhecer e resolver alertas
- Níveis de severidade de alertas
- Informações detalhadas de alertas

#### 📍 Gerenciamento de Localizações
- Estrutura hierárquica de localizações
- Organização edifício/andar/sala
- Gerenciamento de informações de contato
- Coordenadas geográficas

#### 📁 Processamento de Arquivos IFC
- Upload de arquivos de construção IFC
- Extrair espaços de construção
- Processar metadados de construção
- Visualizar estrutura de construção

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/me` - Get current user info

### Sensors
- `GET /api/v1/sensors/` - List sensors with filtering
- `POST /api/v1/sensors/` - Create new sensor
- `GET /api/v1/sensors/{id}` - Get sensor details
- `PUT /api/v1/sensors/{id}` - Update sensor
- `DELETE /api/v1/sensors/{id}` - Delete sensor

### Readings
- `GET /api/v1/readings/` - List readings with filtering
- `POST /api/v1/readings/` - Create reading
- `GET /api/v1/readings/latest` - Get latest readings

### Alerts
- `GET /api/v1/alerts/` - List alerts with filtering
- `PUT /api/v1/alerts/{id}` - Update alert status
- `GET /api/v1/alerts/{id}` - Get alert details

### Locations
- `GET /api/v1/locations/` - List locations
- `POST /api/v1/locations/` - Create location
- `PUT /api/v1/locations/{id}` - Update location
- `DELETE /api/v1/locations/{id}` - Delete location

### IFC Files
- `GET /api/v1/ifc/files` - List IFC files
- `POST /api/v1/ifc/upload` - Upload IFC file
- `GET /api/v1/ifc/files/{id}` - Get IFC file details
- `GET /api/v1/ifc/files/{id}/spaces` - Get spaces from IFC file
- `POST /api/v1/ifc/files/{id}/process` - Reprocess IFC file

## 🛠️ Development

### Project Structure
```
ifc_monitoring_system/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and endpoints
│   ├── auth/               # Authentication and security
│   ├── core/               # Core configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   └── services/           # Business logic services
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   └── services/       # API services
├── uploads/                # File uploads directory
├── main.py                 # Application entry point
├── start_system.py         # Automated startup script
└── create_sample_data.py   # Sample data creation
```

### Adding New Sensor Types

1. Update the sensor type validation in `backend/models/sensor.py`
2. Add simulation logic in `backend/services/monitoring_service.py`
3. Update frontend components in `frontend/src/pages/Sensors.tsx`

### Custom Alert Rules

1. Modify `_check_sensor_thresholds` in `backend/services/monitoring_service.py`
2. Add new alert types to `backend/models/alert.py`
3. Update alert processing logic

### Database Migrations

The system uses SQLAlchemy with automatic table creation. For production:

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## 🧪 Testing

### Backend Testing
```bash
# Run backend tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deploy

### ☁️ Deploy no Heroku (Recomendado)

O método mais fácil e rápido para fazer deploy é usar o Heroku:

#### 🎯 Método 1: Deploy Automático (Mais Fácil)
```bash
# Execute o script de deploy automatizado
python deploy_heroku.py
```
> O script irá guiá-lo através de todo o processo de deploy!

#### 🛠️ Método 2: Deploy Manual
```bash
# 1. Login no Heroku
heroku login

# 2. Criar app
heroku create nome-do-seu-app

# 3. Configurar variáveis
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" -a nome-do-seu-app
heroku config:set DEBUG=False -a nome-do-seu-app

# 4. Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini -a nome-do-seu-app

# 5. Deploy
git push heroku main
```

#### ⚡ Método 3: Deploy via Botão (Mais Rápido)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/seu-usuario/ifc-monitoring-system)

> Clique no botão acima, preencha o nome do app e clique em "Deploy app"!

### 🎨 Configuração do Frontend

Após o deploy do backend, configure o frontend:

1. **🔗 Atualizar URL da API** em `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://seu-app.herokuapp.com/api/v1';
```

2. **🚀 Deploy do Frontend** no Netlify/Vercel:
```bash
cd frontend
npm run build
# Upload da pasta build para Netlify/Vercel
```

### 🧪 Testar o Deploy

Após o deploy, teste se tudo funcionou:

```bash
# Testar se o deploy funcionou
python test_deploy.py
```

### 📊 Monitoramento

```bash
# Ver logs em tempo real
heroku logs --tail -a nome-do-seu-app

# Ver informações do app
heroku apps:info -a nome-do-seu-app

# Reiniciar o app
heroku restart -a nome-do-seu-app
```

### 🏗️ Deploy Tradicional (Alternativo)

Para deploy em servidor próprio:

1. **🔧 Configuração de Ambiente:**
```bash
export DEBUG=False
export DATABASE_URL=postgresql://user:pass@localhost/ifc_monitoring
export SECRET_KEY=your-production-secret-key
```

2. **🗄️ Setup do Banco:**
```bash
createdb ifc_monitoring
alembic upgrade head
```

3. **🏗️ Build do Frontend:**
```bash
cd frontend && npm run build
```

4. **🚀 Deploy do Backend:**
```bash
# Com Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Com Docker
docker build -t ifc-monitoring .
docker run -p 8000:8000 ifc-monitoring
```

## 📊 Monitoramento

### 🏥 Saúde do Sistema
- **Health Check**: `GET /health` - Verifica se o sistema está funcionando
- **Métricas da API**: Disponíveis via endpoints específicos
- **Logs Configurados**: Para monitoramento de produção

### ⚡ Performance
- **Otimização de Consultas**: Banco de dados otimizado
- **Cache de Dados**: Cache para dados frequentemente acessados
- **Processamento em Background**: Tarefas automatizadas

## 🤝 Contribuindo

1. **🍴 Fork** o repositório
2. **🌿 Criar branch** (`git checkout -b feature/amazing-feature`)
3. **💾 Commit** suas mudanças (`git commit -m 'Add amazing feature'`)
4. **📤 Push** para a branch (`git push origin feature/amazing-feature`)
5. **🔀 Abrir Pull Request**

### 📋 Diretrizes de Desenvolvimento
- **Python**: Seguir PEP 8 para código Python
- **Frontend**: Usar TypeScript para desenvolvimento frontend
- **Testes**: Escrever testes para novas funcionalidades
- **Documentação**: Atualizar documentação para mudanças na API

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **📚 Documentação**: Consulte este README e documentação da API em `/docs`
- **🐛 Issues**: Crie uma issue no GitHub
- **💬 Discussões**: Use GitHub Discussions para perguntas

## 🔮 Roadmap

### 🚀 Funcionalidades Planejadas
- [ ] **🔌 Conexões WebSocket em tempo real**
- [ ] **📊 Visualização avançada de dados**
- [ ] **📱 Aplicativo móvel**
- [ ] **🤖 Machine learning para alertas preditivos**
- [ ] **🌐 Integração com redes de sensores externos**
- [ ] **🏗️ Visualização avançada de IFC**
- [ ] **🏢 Suporte multi-tenant**
- [ ] **📈 Relatórios e análises avançadas**

## 📁 Arquivos de Deploy

O projeto inclui os seguintes arquivos para facilitar o deploy:

- **`deploy_heroku.py`** - Script de deploy automático
- **`setup_database.py`** - Configuração do banco de dados
- **`test_deploy.py`** - Teste do deploy
- **`Procfile`** - Configuração do Heroku
- **`runtime.txt`** - Versão do Python
- **`app.json`** - Configuração para deploy via botão

## 🎉 Pronto para Usar!

Seu sistema IFC Monitoring está agora completamente configurado e pronto para deploy! 

**Deploy em 3 passos simples:**
1. Clone o repositório
2. Execute `python deploy_heroku.py`
3. Acesse seu app em `https://seu-app.herokuapp.com`

---

**Construído com ❤️ para monitoramento de instalações industriais**
