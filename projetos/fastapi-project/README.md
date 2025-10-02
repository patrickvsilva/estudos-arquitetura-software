# Projeto: API REST com FastAPI

## Objetivo

Criar uma API REST moderna, bem estruturada e seguindo boas práticas de arquitetura de software usando FastAPI.

## Estrutura do Projeto

```
fastapi-project/
├── README.md                 # Este arquivo
├── app/                     # Código da aplicação
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da aplicação
│   ├── api/                # Endpoints da API
│   │   ├── __init__.py
│   │   ├── v1/             # Versão 1 da API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/  # Endpoints organizados por recurso
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   └── items.py
│   │   │   └── api.py      # Router principal da v1
│   │   └── deps.py         # Dependências compartilhadas
│   ├── core/               # Configurações e utilitários core
│   │   ├── __init__.py
│   │   ├── config.py       # Configurações da aplicação
│   │   └── security.py     # Segurança e autenticação
│   ├── db/                 # Database
│   │   ├── __init__.py
│   │   ├── base.py         # Base do SQLAlchemy
│   │   └── session.py      # Sessão do banco
│   ├── models/             # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/            # Schemas Pydantic (DTOs)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/           # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── repositories/       # Camada de dados
│       ├── __init__.py
│       ├── base.py
│       ├── user_repository.py
│       └── item_repository.py
├── tests/                  # Testes
│   ├── __init__.py
│   ├── conftest.py         # Fixtures do pytest
│   ├── api/
│   │   └── test_users.py
│   └── services/
│       └── test_user_service.py
├── alembic/                # Migrações de banco
│   └── versions/
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências
├── pyproject.toml         # Configuração do projeto
└── docker-compose.yml     # Containers Docker
```

## Arquitetura

O projeto segue uma arquitetura em camadas (Layered Architecture):

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │  ← Endpoints, validação request/response
├─────────────────────────────────────┤
│        Service Layer                │  ← Lógica de negócio
├─────────────────────────────────────┤
│       Repository Layer              │  ← Acesso a dados
├─────────────────────────────────────┤
│      Database (PostgreSQL)          │  ← Persistência
└─────────────────────────────────────┘
```

### Camadas

1. **API Layer**: Recebe requisições HTTP, valida entrada, chama serviços
2. **Service Layer**: Implementa regras de negócio, orquestra operações
3. **Repository Layer**: Abstrai acesso a dados, queries ao banco
4. **Database**: Armazena dados persistentes

## Funcionalidades

### 1. CRUD de Usuários
- [x] Criar usuário
- [x] Listar usuários
- [x] Obter usuário por ID
- [x] Atualizar usuário
- [x] Deletar usuário

### 2. CRUD de Items
- [x] Criar item
- [x] Listar items
- [x] Obter item por ID
- [x] Atualizar item
- [x] Deletar item

### 3. Autenticação
- [ ] Registro de usuário
- [ ] Login (JWT)
- [ ] Refresh token
- [ ] Proteção de rotas

### 4. Documentação
- [x] Swagger UI (automático)
- [x] ReDoc (automático)
- [ ] Documentação adicional

## Exemplo de Código

### 1. Model (SQLAlchemy)

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
```

### 2. Schema (Pydantic)

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True
```

### 3. Repository

```python
# app/repositories/user_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Busca usuário por email."""
        return db.query(User).filter(User.email == email).first()
    
    def get_active_users(self, db: Session) -> List[User]:
        """Retorna apenas usuários ativos."""
        return db.query(User).filter(User.is_active == True).all()

user_repository = UserRepository(User)
```

### 4. Service

```python
# app/services/user_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.core.security import get_password_hash

class UserService:
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """Cria novo usuário."""
        # Verificar se email já existe
        existing_user = user_repository.get_by_email(db, user_in.email)
        if existing_user:
            raise ValueError("Email já cadastrado")
        
        # Hash da senha
        hashed_password = get_password_hash(user_in.password)
        
        # Criar usuário
        user_data = user_in.dict(exclude={'password'})
        user_data['hashed_password'] = hashed_password
        
        return user_repository.create(db, obj_in=user_data)
    
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        """Busca usuário por ID."""
        return user_repository.get(db, id=user_id)
    
    def list_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista usuários."""
        return user_repository.get_multi(db, skip=skip, limit=limit)

user_service = UserService()
```

### 5. Endpoint

```python
# app/api/v1/endpoints/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserCreate, UserInDB
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Cria novo usuário.
    """
    try:
        user = user_service.create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserInDB)
def get_user(
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Busca usuário por ID.
    """
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.get("/", response_model=List[UserInDB])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """
    Lista todos os usuários.
    """
    users = user_service.list_users(db, skip=skip, limit=limit)
    return users
```

### 6. Main Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "API está funcionando!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Como Usar

### 1. Configurar Ambiente

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar exemplo
cp .env.example .env

# Editar .env com suas configurações
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
```

### 3. Executar Migrações

```bash
# Criar migração
alembic revision --autogenerate -m "Initial migration"

# Aplicar migração
alembic upgrade head
```

### 4. Executar Aplicação

```bash
# Desenvolvimento
uvicorn app.main:app --reload

# Produção
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 5. Acessar Documentação

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6. Executar Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=app tests/

# Testes específicos
pytest tests/api/test_users.py -v
```

## Boas Práticas Implementadas

✅ **Arquitetura em Camadas**
- Separação clara de responsabilidades
- Baixo acoplamento entre camadas

✅ **Dependency Injection**
- Uso de Depends do FastAPI
- Facilita testes e manutenção

✅ **Type Hints**
- Código totalmente tipado
- Validação automática com Pydantic

✅ **Documentação Automática**
- OpenAPI/Swagger gerado automaticamente
- Schemas documentados

✅ **Tratamento de Erros**
- Exceções HTTP apropriadas
- Mensagens de erro claras

✅ **Validação de Dados**
- Pydantic schemas
- Validação na entrada e saída

✅ **Testes Automatizados**
- Testes unitários
- Testes de integração
- Fixtures do pytest

✅ **Configuração**
- Variáveis de ambiente
- Configuração centralizada

✅ **Segurança**
- Hash de senhas
- JWT para autenticação
- CORS configurado

## Tecnologias

- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM
- **Alembic**: Migrações de banco
- **Pydantic**: Validação de dados
- **pytest**: Framework de testes
- **PostgreSQL**: Banco de dados
- **Docker**: Containerização

## Próximos Passos

- [ ] Implementar autenticação JWT
- [ ] Adicionar rate limiting
- [ ] Implementar cache (Redis)
- [ ] Adicionar background tasks (Celery)
- [ ] Implementar paginação avançada
- [ ] Adicionar filtros e ordenação
- [ ] Implementar versionamento de API
- [ ] Configurar CI/CD
- [ ] Deploy em cloud (AWS/GCP/Azure)

## Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-postgresql)
