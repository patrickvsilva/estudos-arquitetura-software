# Clean Architecture (Arquitetura Limpa)

## Introdução

Clean Architecture é um padrão arquitetural proposto por Robert C. Martin (Uncle Bob) que enfatiza a separação de responsabilidades através de camadas bem definidas.

## Princípio Fundamental

**"A arquitetura deve ser independente de frameworks, UI, banco de dados e agentes externos."**

## As Camadas

A Clean Architecture é organizada em camadas concêntricas, onde as dependências apontam apenas para dentro (das camadas externas para as internas).

```
┌─────────────────────────────────────────┐
│  Frameworks & Drivers (UI, DB, Web)    │
│  ┌───────────────────────────────────┐  │
│  │  Interface Adapters              │  │
│  │  (Controllers, Presenters, Gateways)│
│  │  ┌───────────────────────────┐   │  │
│  │  │  Application Business     │   │  │
│  │  │  Rules (Use Cases)        │   │  │
│  │  │  ┌─────────────────────┐  │   │  │
│  │  │  │  Enterprise Business│  │   │  │
│  │  │  │  Rules (Entities)   │  │   │  │
│  │  │  └─────────────────────┘  │   │  │
│  │  └───────────────────────────┘   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 1. Entities (Entidades - Centro)
- **O que é**: Lógica de negócio fundamental da empresa
- **Características**: Independente de qualquer coisa externa
- **Exemplo**: Regras de domínio que existiriam mesmo sem software

```python
# entities/order.py
from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class Order:
    """Entidade de domínio: Pedido."""
    id: int
    customer_id: int
    items: List['OrderItem']
    
    def calculate_total(self) -> Decimal:
        """Regra de negócio: cálculo do total."""
        return sum(item.get_subtotal() for item in self.items)
    
    def can_be_cancelled(self) -> bool:
        """Regra de negócio: pedido pode ser cancelado."""
        return self.status in ['pending', 'processing']
```

### 2. Use Cases (Casos de Uso)
- **O que é**: Lógica de aplicação específica
- **Características**: Orquestra o fluxo de dados entre entidades
- **Exemplo**: "Criar pedido", "Cancelar pedido"

```python
# use_cases/create_order.py
from typing import Protocol
from entities.order import Order
from dto.order_dto import CreateOrderDTO

class OrderRepository(Protocol):
    """Interface do repositório (Dependency Inversion)."""
    def save(self, order: Order) -> Order:
        ...

class CreateOrderUseCase:
    """Caso de uso: Criar pedido."""
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def execute(self, dto: CreateOrderDTO) -> Order:
        """
        Executa o caso de uso de criar pedido.
        
        Args:
            dto: Dados para criação do pedido
            
        Returns:
            Pedido criado
            
        Raises:
            ValueError: Se dados inválidos
        """
        # Validar dados
        if not dto.items:
            raise ValueError("Pedido deve ter itens")
        
        # Criar entidade
        order = Order(
            id=None,
            customer_id=dto.customer_id,
            items=dto.items
        )
        
        # Aplicar regras de negócio
        if order.calculate_total() < 0:
            raise ValueError("Total do pedido inválido")
        
        # Persistir
        saved_order = self.order_repository.save(order)
        
        return saved_order
```

### 3. Interface Adapters (Adaptadores)
- **O que é**: Conversão entre casos de uso e mundo externo
- **Características**: Controllers, Presenters, Gateways
- **Exemplo**: Adaptar requisição HTTP para DTO

```python
# adapters/controllers/order_controller.py
from use_cases.create_order import CreateOrderUseCase
from dto.order_dto import CreateOrderDTO

class OrderController:
    """Controller que adapta HTTP para caso de uso."""
    
    def __init__(self, create_order_use_case: CreateOrderUseCase):
        self.create_order = create_order_use_case
    
    def create(self, request_data: dict) -> dict:
        """
        Endpoint HTTP POST /orders
        
        Adapta requisição HTTP para o caso de uso.
        """
        try:
            # Converter request HTTP para DTO
            dto = CreateOrderDTO(
                customer_id=request_data['customer_id'],
                items=request_data['items']
            )
            
            # Executar caso de uso
            order = self.create_order.execute(dto)
            
            # Converter resultado para response HTTP
            return {
                'success': True,
                'order_id': order.id,
                'total': float(order.calculate_total())
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
```

### 4. Frameworks & Drivers (Camada Externa)
- **O que é**: Detalhes de implementação (DB, Web, UI)
- **Características**: Mais externa, mais volátil
- **Exemplo**: FastAPI, SQLAlchemy, frameworks específicos

```python
# infrastructure/web/fastapi_app.py
from fastapi import FastAPI, Depends
from adapters.controllers.order_controller import OrderController
from infrastructure.repositories.sql_order_repository import SQLOrderRepository
from use_cases.create_order import CreateOrderUseCase

app = FastAPI()

def get_order_controller() -> OrderController:
    """Dependency injection."""
    repository = SQLOrderRepository()
    use_case = CreateOrderUseCase(repository)
    return OrderController(use_case)

@app.post("/orders")
def create_order(
    request_data: dict,
    controller: OrderController = Depends(get_order_controller)
):
    """Endpoint FastAPI."""
    return controller.create(request_data)
```

## Benefícios

### 1. Independência de Frameworks
```python
# Fácil trocar de FastAPI para Flask
# Apenas muda a camada externa, use cases permanecem iguais
```

### 2. Testabilidade
```python
# Testar use case sem framework web
def test_create_order_use_case():
    # Mock do repositório
    mock_repo = MockOrderRepository()
    use_case = CreateOrderUseCase(mock_repo)
    
    # Testar lógica pura
    result = use_case.execute(dto)
    assert result.id is not None
```

### 3. Independência de UI
```python
# Mesmo use case para:
# - API REST
# - GraphQL
# - CLI
# - GUI
```

### 4. Independência de Banco de Dados
```python
# Trocar PostgreSQL por MongoDB
# Apenas implementa novo repositório
class MongoOrderRepository:
    def save(self, order: Order) -> Order:
        # Implementação MongoDB
        pass
```

## Exemplo Completo

```python
# 1. ENTITIES (Centro)
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
    
    def is_valid(self) -> bool:
        return self.price > 0

# 2. USE CASES
from typing import Protocol

class ProductRepository(Protocol):
    def get_by_id(self, id: int) -> Product: ...
    def save(self, product: Product) -> Product: ...

class UpdateProductPriceUseCase:
    def __init__(self, repo: ProductRepository):
        self.repo = repo
    
    def execute(self, product_id: int, new_price: float) -> Product:
        product = self.repo.get_by_id(product_id)
        product.price = new_price
        
        if not product.is_valid():
            raise ValueError("Preço inválido")
        
        return self.repo.save(product)

# 3. ADAPTERS
class ProductController:
    def __init__(self, use_case: UpdateProductPriceUseCase):
        self.use_case = use_case
    
    def update_price(self, request: dict) -> dict:
        try:
            product = self.use_case.execute(
                request['id'],
                request['price']
            )
            return {'success': True, 'product': product}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# 4. FRAMEWORKS (Externo)
class SQLProductRepository:
    def get_by_id(self, id: int) -> Product:
        # Implementação com SQLAlchemy
        pass
    
    def save(self, product: Product) -> Product:
        # Implementação com SQLAlchemy
        pass
```

## Regras de Dependência

### ✅ CORRETO
```python
# Camadas externas dependem das internas
from entities.order import Order  # ✓
from use_cases.create_order import CreateOrderUseCase  # ✓

class OrderController:
    def __init__(self, use_case: CreateOrderUseCase):
        self.use_case = use_case
```

### ❌ ERRADO
```python
# Camadas internas NÃO devem depender das externas
# entities/order.py
from infrastructure.repositories.sql_repository import SQLRepository  # ✗

class Order:
    def save(self):
        repo = SQLRepository()  # ✗ Dependência invertida!
        repo.save(self)
```

## Dependency Inversion

Use interfaces (Protocols) para inverter dependências:

```python
# use_cases/send_email.py
from typing import Protocol

class EmailService(Protocol):
    """Interface - camada interna define o contrato."""
    def send(self, to: str, subject: str, body: str) -> None:
        ...

class SendWelcomeEmailUseCase:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service  # Depende da abstração

# infrastructure/email/smtp_service.py
class SMTPEmailService:
    """Implementação concreta - camada externa."""
    def send(self, to: str, subject: str, body: str) -> None:
        # Implementação com SMTP
        pass
```

## Quando Usar

✅ **Use Clean Architecture quando:**
- Projeto de médio a grande porte
- Múltiplas interfaces (Web API, CLI, Desktop)
- Lógica de negócio complexa
- Necessidade de alta testabilidade
- Equipe grande/distribuída

❌ **Não use quando:**
- Projeto muito simples (CRUD básico)
- Protótipo rápido
- Script utilitário
- Overhead não justifica benefícios

## Resumo

**4 Camadas:**
1. **Entities**: Lógica de negócio fundamental
2. **Use Cases**: Lógica de aplicação
3. **Adapters**: Conversão de dados
4. **Frameworks**: Detalhes de implementação

**Regra de Ouro:**
- Dependências apontam para dentro
- Camadas internas desconhecem as externas
- Use interfaces para inverter dependências

## Recursos

- Livro: "Clean Architecture" - Robert C. Martin
- Blog: [The Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- Exemplo: [Python Clean Architecture](https://github.com/cosmicpython/book)
