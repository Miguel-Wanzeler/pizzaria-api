# Pizzaria API

API REST para gerenciamento de pedidos, construída com FastAPI. Possui cadastro e login de usuários com autenticação JWT, criação de pedidos, itens com cálculo automático de preço e controle de acesso por perfil (usuário comum e administrador).

## Tecnologias

- Python 3
- FastAPI
- SQLAlchemy (ORM) + SQLite
- Alembic (migrações)
- JWT com `python-jose`
- Hash de senha com `passlib` (bcrypt)
- `python-dotenv` (variáveis de ambiente)

## Funcionalidades

- Cadastro de usuários com validação de senha e hash com bcrypt
- Login com access token e refresh token (JWT)
- Criação, cancelamento e finalização de pedidos
- Adição e remoção de itens, com recálculo automático do preço total
- Permissões: o usuário só acessa os próprios pedidos; o administrador acessa todos

## Como rodar

1. Clone o repositório e entre na pasta:

```bash
git clone <url-do-repositorio>
cd <nome-da-pasta>
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` a partir do exemplo e preencha os valores:

```bash
cp .env.example .env
```

```
SECRET_KEY=sua_chave_secreta
ALGORITM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Para gerar uma chave segura:

```bash
openssl rand -hex 32
```

5. Crie o banco de dados com as migrações:

```bash
alembic upgrade head
```

6. Inicie o servidor:

```bash
uvicorn main:app --reload
```

A documentação interativa fica disponível em `http://127.0.0.1:8000/docs`.

## Endpoints

### Autenticação (`/auth`)

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/criar_conta` | Cria um novo usuário |
| POST | `/auth/login` | Login com e-mail e senha (retorna access e refresh token) |
| POST | `/auth/login-form` | Login via formulário OAuth2 (usado pelo botão Authorize do `/docs`) |
| GET | `/auth/refresh` | Gera um novo access token a partir do refresh token |

### Pedidos (`/pedidos`) — requer token

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/pedidos/pedido` | Cria um pedido para o usuário logado |
| GET | `/pedidos/pedido/{id_pedido}` | Visualiza um pedido |
| POST | `/pedidos/pedido/cancelar/{id_pedido}` | Cancela um pedido |
| POST | `/pedidos/pedido/finalizar/{id_pedido}` | Finaliza um pedido |
| POST | `/pedidos/pedido/adicionar-item/{id_pedido}` | Adiciona um item ao pedido |
| POST | `/pedidos/pedido/remover-item/{id_item_pedido}` | Remove um item do pedido |
| GET | `/pedidos/listar` | Lista todos os pedidos (somente admin) |
| GET | `/pedidos/listar/pedidos-usuario` | Lista os pedidos do usuário logado |

## Estrutura do projeto

```
├── alembic/            # Migrações do banco
├── main.py             # Inicialização do app e configurações
├── models.py           # Modelos do banco (Usuario, Pedido, ItemPedido)
├── schemas.py          # Schemas Pydantic (entrada e saída)
├── dependencies.py     # Sessão do banco e verificação de token
├── auth_routes.py      # Rotas de autenticação
├── order_routes.py     # Rotas de pedidos
└── alembic.ini
```
