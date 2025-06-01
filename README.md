# API Vitivinicultura Embrapa

API REST para coleta e análise de dados do setor vitivinícola brasileiro, com foco em aplicações de Machine Learning.

## 🌟 Características

- Dados estruturados da Embrapa Uva e Vinho
- Autenticação JWT
- Documentação automática (Swagger/OpenAPI)
- Preparado para ML com features pré-processadas
- Docker ready
- CORS habilitado

## 🚀 Endpoints

- `/producao`: Dados históricos de produção
- `/processamento`: Informações de processamento
- `/comercializacao`: Dados de mercado
- `/importacao`: Estatísticas de importação
- `/exportacao`: Dados de exportação

Cada endpoint retorna dados no formato:
```json
[
    {
        "data": [...],  // Lista de registros
        "features": [...],  // Lista de todas as colunas
        "numeric_features": [...]  // Lista de colunas numéricas
    }
]
```

## 🛠️ Tecnologias

- FastAPI
- Pandas
- BeautifulSoup4
- JWT Authentication
- Docker

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/vitivinicultura-api.git
cd vitivinicultura-api
```

2. Configure as variáveis de ambiente:
```bash
# Linux/Mac
export SECRET_KEY="sua_chave_secreta_aqui"

# Windows (PowerShell)
$env:SECRET_KEY="sua_chave_secreta_aqui"
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a API:
```bash
uvicorn main:app --reload
```

## 🔒 Autenticação

1. Obtenha um token:
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=testpass"
```

2. Use o token:
```bash
curl -X GET "http://localhost:8000/producao" \
     -H "Authorization: Bearer seu_token_aqui"
```

## 🐳 Docker

1. Configure as variáveis de ambiente:
```bash
echo "SECRET_KEY=sua_chave_secreta_aqui" > .env
```

2. Construa a imagem:
```bash
docker build -t vitivinicultura-api .
```

3. Execute o container:
```bash
docker run -p 8000:8000 --env-file .env vitivinicultura-api
```

## 🏗️ Arquitetura

```
├── API (FastAPI)
│   ├── Autenticação JWT
│   ├── Validação de dados
│   └── Documentação OpenAPI
│
├── Scraping
│   ├── Coleta de dados (BeautifulSoup4)
│   ├── Processamento (Pandas)
│   └── Normalização
│
└── ML Ready
    ├── Features pré-processadas
    ├── Metadados
    └── Formato padronizado
```

## 🎯 Uso em Machine Learning

Esta API foi projetada para alimentar modelos de ML para:

1. Previsão de Produção
   - Análise de séries temporais
   - Previsão de safra

2. Análise de Mercado
   - Tendências de preços
   - Oportunidades de exportação

3. Otimização de Processos
   - Eficiência no processamento
   - Gestão de estoque

## 📊 Exemplo de Uso em Python

```python
import requests
import pandas as pd

# Autenticação
auth_response = requests.post(
    "http://localhost:8000/token",
    data={"username": "testuser", "password": "testpass"}
)
token = auth_response.json()["access_token"]

# Headers com token
headers = {"Authorization": f"Bearer {token}"}

# Coleta de dados
response = requests.get("http://localhost:8000/producao", headers=headers)
data = response.json()

# Criação do DataFrame
df = pd.DataFrame(data[0]["data"])  # Primeiro conjunto de dados

# Features disponíveis
all_features = data[0]["features"]
numeric_features = data[0]["numeric_features"]

# Preparação para ML
X = df[numeric_features]  # Features numéricas
```

## 🔐 Segurança

Em produção:
1. Use uma chave secreta forte
2. Configure CORS apropriadamente
3. Use HTTPS
4. Implemente rate limiting

## 📝 Licença

MIT

## 👥 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request 