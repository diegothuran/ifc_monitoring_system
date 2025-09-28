# Configuração do Frontend para Heroku

## Atualizar API URL

Após fazer o deploy do backend no Heroku, você precisa atualizar o frontend para se conectar à nova URL.

### 1. Atualizar arquivo de configuração da API

Edite o arquivo `frontend/src/services/api.ts`:

```typescript
// Configuração para produção (Heroku)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://seu-app.herokuapp.com/api/v1';

// Configuração para desenvolvimento
// const API_BASE_URL = 'https://ifc-backend-ph0n.onrender.com/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 2. Criar arquivo .env no frontend

Crie o arquivo `frontend/.env`:

```bash
REACT_APP_API_URL=https://seu-app.herokuapp.com/api/v1
```

### 3. Deploy do Frontend

#### Opção A: Netlify (Recomendado)

1. Faça push do frontend para o GitHub
2. Conecte o repositório ao Netlify
3. Configure as variáveis de ambiente:
   - `REACT_APP_API_URL`: `https://seu-app.herokuapp.com/api/v1`

#### Opção B: Vercel

1. Faça push do frontend para o GitHub
2. Conecte o repositório ao Vercel
3. Configure as variáveis de ambiente:
   - `REACT_APP_API_URL`: `https://seu-app.herokuapp.com/api/v1`

#### Opção C: Heroku (Frontend também)

1. Crie um novo app no Heroku para o frontend
2. Configure o buildpack para Node.js
3. Adicione o arquivo `package.json` com scripts de build
4. Configure as variáveis de ambiente

### 4. Scripts de Build

Adicione ao `frontend/package.json`:

```json
{
  "scripts": {
    "build": "react-scripts build",
    "start": "react-scripts start",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

### 5. Arquivo de configuração dinâmica

Crie `frontend/src/config.js`:

```javascript
const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'https://seu-app.herokuapp.com/api/v1',
  environment: process.env.NODE_ENV || 'development'
};

export default config;
```

### 6. Atualizar imports

No `frontend/src/services/api.ts`:

```typescript
import config from '../config';

export const api = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## Teste da Conexão

Após configurar, teste se o frontend consegue se conectar ao backend:

1. Abra o console do navegador
2. Verifique se não há erros de CORS
3. Teste uma requisição da API
4. Verifique se os dados estão sendo carregados

## Troubleshooting

### Erro de CORS
- Verifique se o backend está configurado para aceitar o domínio do frontend
- Confirme se a URL da API está correta

### Erro 404
- Verifique se a URL da API está correta
- Confirme se o backend está rodando

### Erro de Autenticação
- Verifique se o token JWT está sendo enviado corretamente
- Confirme se as rotas de autenticação estão funcionando

---

✅ **Frontend configurado!** Agora seu sistema completo está rodando na nuvem!
