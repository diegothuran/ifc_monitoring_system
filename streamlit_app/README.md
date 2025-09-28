# IFC Monitoring System - Streamlit Frontend

Uma interface web moderna e intuitiva para o sistema de monitoramento IFC (Industrial Facility Condition) construída com Streamlit.

## 🚀 Características

- **Dashboard em Tempo Real**: Visualização de métricas e gráficos atualizados automaticamente
- **Gestão de Sensores**: Interface completa para gerenciar sensores e suas configurações
- **Sistema de Alertas**: Monitoramento e gestão de alertas com diferentes níveis de severidade
- **Localizações**: Organização hierárquica de sensores por localização
- **Análise de Dados**: Gráficos interativos e relatórios de leituras dos sensores
- **🏗️ Upload de Arquivos IFC**: Carregamento e processamento de plantas 3D
- **🌐 Visualização 3D**: Visualização interativa de plantas e espaços
- **Autenticação**: Sistema de login seguro com JWT
- **Interface Responsiva**: Design moderno e intuitivo

## 📋 Pré-requisitos

- Python 3.8+
- Backend IFC Monitoring System rodando (FastAPI)
- PostgreSQL (configurado no backend)

## 🛠️ Instalação

### Método 1: Execução Direta

```bash
# Navegue para o diretório streamlit_app
cd streamlit_app

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
streamlit run main.py
```

### Método 2: Usando o Script de Execução

```bash
# Navegue para o diretório streamlit_app
cd streamlit_app

# Execute o script (instala dependências e inicia automaticamente)
python run.py
```

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `streamlit_app`:

```env
# URL do backend API
API_BASE_URL=https://ifc-backend-ph0n.onrender.com/api/v1

# Configurações do Streamlit (opcional)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Configuração do Backend

Certifique-se de que o backend está rodando na porta 8000:

```bash
# No diretório raiz do projeto
python main.py
```

## 📱 Como Usar

### 1. Login

- Acesse http://localhost:8501
- Use as credenciais de usuário cadastradas no sistema
- O sistema suporta diferentes roles: Admin, Operator, Viewer

### 2. Dashboard

- **Visão Geral**: Métricas principais do sistema
- **Gráficos em Tempo Real**: Temperatura, umidade e outros parâmetros
- **Alertas Recentes**: Lista dos alertas mais recentes
- **Auto-refresh**: Atualização automática dos dados

### 3. Gestão de Sensores

- **Lista de Sensores**: Visualização de todos os sensores cadastrados
- **Adicionar Sensor**: Formulário para cadastro de novos sensores
- **Configurações**: Definir tipos, localizações e parâmetros

### 4. Sistema de Alertas

- **Filtros**: Por status e severidade
- **Ações**: Reconhecer, resolver e gerenciar alertas
- **Relatórios**: Exportação de dados de alertas

### 5. Localizações

- **Organização**: Estrutura hierárquica (edifício → andar → sala)
- **Responsáveis**: Atribuição de pessoas responsáveis
- **Contatos**: Informações de contato para cada localização

### 6. Análise de Leituras

- **Período**: Seleção de data início e fim
- **Gráficos**: Visualização temporal dos dados
- **Exportação**: Download dos dados em CSV

### 7. 🏗️ Plantas IFC (NOVO!)

#### Upload de Arquivos
- **Formatos Suportados**: .ifc (máximo 100MB)
- **Processamento Automático**: Extração de espaços e metadados
- **Status de Processamento**: Acompanhamento em tempo real

#### Visualização 3D
- **Visualização Interativa**: Gráficos 3D com Plotly
- **Planta Baixa**: Visualização 2D dos espaços
- **Informações Detalhadas**: Hover com dados dos espaços

#### Gestão de Espaços
- **Lista de Espaços**: Todos os espaços extraídos do IFC
- **Metadados**: Área, volume, coordenadas, tipo de uso
- **Estatísticas**: Resumo de espaços por planta

## 🎨 Personalização

### Cores e Temas

Edite o arquivo `config.py` para personalizar:

```python
# Cores do gráfico
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728'
}

# Cores de severidade de alertas
ALERT_COLORS = {
    'low': '#17becf',
    'medium': '#ff7f0e',
    'high': '#d62728',
    'critical': '#8b0000'
}
```

### Tipos de Sensores

Adicione novos tipos de sensores em `config.py`:

```python
SENSOR_TYPES = {
    'new_sensor_type': {
        'name': 'Novo Tipo',
        'unit': 'unidade',
        'icon': '🔧',
        'color': '#color'
    }
}
```

## 📊 Funcionalidades Avançadas

### Auto-refresh

O dashboard atualiza automaticamente a cada 30 segundos (configurável):

```python
# Em config.py
AUTO_REFRESH_INTERVAL = 30  # segundos
```

### Gráficos Interativos

- **Plotly**: Gráficos totalmente interativos
- **Zoom**: Funcionalidade de zoom e pan
- **Hover**: Informações detalhadas ao passar o mouse
- **Exportação**: Download de gráficos como PNG

### Visualização IFC

- **Processamento Assíncrono**: Upload e processamento em background
- **Extração Automática**: Metadados e espaços extraídos automaticamente
- **Visualização 3D**: Gráficos interativos com coordenadas reais
- **Múltiplos Arquivos**: Suporte a várias plantas simultaneamente

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de Conexão com API**
   ```
   Solução: Verifique se o backend está rodando na porta 8000
   ```

2. **Erro de Autenticação**
   ```
   Solução: Verifique as credenciais e se o usuário está ativo no sistema
   ```

3. **Dados Não Carregam**
   ```
   Solução: Verifique a conexão com o banco de dados no backend
   ```

4. **Erro no Upload de IFC**
   ```
   Solução: Verifique se o arquivo é válido e não excede 100MB
   ```

### Logs

Para debug, execute com verbose:

```bash
streamlit run main.py --logger.level=debug
```

## 🚀 Deploy

### Deploy Local com Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Deploy em Cloud

Para deploy em serviços como Heroku, Railway, ou similar:

1. Crie um arquivo `Procfile`:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Configure as variáveis de ambiente:
   ```
   API_BASE_URL=https://your-backend-url.com/api/v1
   ```

## 📈 Próximas Funcionalidades

- [ ] Notificações push em tempo real
- [ ] Relatórios PDF automáticos
- [ ] Integração com WhatsApp/SMS
- [ ] Machine Learning para predição
- [ ] Dashboard personalizável por usuário
- [ ] Integração com sistemas externos (SCADA, PLC)
- [ ] **Mapeamento de sensores na planta 3D**
- [ ] **Exportação de plantas em diferentes formatos**
- [ ] **Análise de performance baseada na planta**

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Email: suporte@ifc-monitoring.com
- Issues: Use o sistema de issues do GitHub
- Documentação: Consulte a documentação da API no backend