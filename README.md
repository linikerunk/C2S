# FastAPI MCP Project

Este projeto implementa uma aplicação cliente-servidor utilizando FastAPI e o Protocolo MCP (Message Communication Protocol). A aplicação é composta por um servidor que expõe uma API, um banco de dados SQLite e um agente virtual que interage com o usuário através do terminal.

## Estrutura do Projeto

```
mcp-communication/
├── app/
│   ├── main.py               # Ponto de entrada da aplicação FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py      # Define as rotas da API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Configurações da aplicação
│   │   ├── database.py       # Configuração do banco de dados
│   │   └── init_db.py        # Script de inicialização do banco
│   ├── models/
│   │   ├── __init__.py
│   │   └── vehicle.py        # Modelo de dados dos veículos
│   └── schemas/
│       ├── __init__.py
│       └── vehicle.py        # Schemas Pydantic
├── terminal_app/
│   ├── __init__.py
│   ├── agent.py             # Agente virtual com OpenAI
│   ├── config.py            # Configurações do agente
│   └── styles.py            # Estilos do terminal
├── mock_data/
│   ├── __init__.py
│   └── migrate_db.py        # Script de migração com dados
├── requirements.txt
└── README.md
```

## Instalação

OPENAI_API_KEY=<your-api-key> no .env vc deve adicionar sua chave open ai

1. Clone o repositório e instale as dependências:
```bash
git clone <repository-url>
cd mcp-communication
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Inicialização do Banco de Dados

1. Primeiro, crie as tabelas do banco:
```bash
python -m app.core.init_db
```

2. Em seguida, execute a migração para popular o banco com dados:
```bash
python -m mock_data.migrate_db
```

3. Verifique se o banco foi criado corretamente:
```bash
sqlite3 C2S
.tables
.schema vehicles
.quit
```

## Execução da Aplicação

1. Inicie o servidor FastAPI:
```bash
uvicorn app.main:app --reload
```
O servidor estará disponível em `http://127.0.0.1:8000`

2. Em outro terminal, inicie o agente virtual:
```bash
python -m terminal_app.agent
```

## APIs Disponíveis

- `GET /api/v1/vehicles` - Lista todos os veículos
- `GET /api/v1/vehicles/{id}` - Obtém um veículo específico
- `POST /api/v1/vehicles` - Cadastra um novo veículo

## Funcionalidades do Agente Virtual

O agente virtual oferece:
- Consulta de veículos por marca/modelo
- Comparação entre veículos
- Informações técnicas detalhadas
- Sugestões personalizadas

## Contribuição

Para contribuir:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature'`)
4. Push para a branch (`git push origin feature/nome`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.